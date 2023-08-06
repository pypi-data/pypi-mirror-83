from typing import Dict, List
from urllib.parse import urlencode
import json
import requests
import urllib3


class Aqua():

    def __init__(self, id: str = None, password: str = None, host: str = None, port: str = '443',
                 api_version: str = 'v1', \
                 using_tls=True, verify_tls: bool = False, cacert_file: str = None, proxy=None, remember: bool = False,
                 token: str = None):
        """
        Currently both v1 and v2 calls are abstracted in this client. You currently do not need to specify API version to
        make v2 calls.

        Args:
            id: username
            password: password
            host: CSP console/API server IP address
            port:  CSP console/API server port
            api_version: optional. currently at v1
            using_ssl: optional. used to hit https urls
            verify_tls: optional. Whether to validate certificate. Set to false for self signed certs.
            cacert_file: optional CA certificates to trust for certificate verification
            proxy: optional http/https proxy dictionary
            remember: whether to create an extended 30 day session; if false session token will be valid for 9 hours

        :return: an Aqua object that represents API endpoint and used for all subsequent calls.
        """

        self.api_version = api_version
        self.verify_tls = verify_tls
        if self.verify_tls is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.id = id
        self.proxy = proxy
        self.host = host
        self.port = port
        self.remember = remember
        self.headers = {'Content-Type': 'application/json', 'api-version': self.api_version}
        self.url_prefix = 'http{}://{}:{}/api/{}'.format('s' if using_tls else '', self.host, self.port,
                                                         self.api_version)
        if token is not None:
            self.token = token
            self.headers['Authorization'] = f"Bearer {self.token}"
        else:
            self._auth(password)

    def _auth(self, password):
        url = "{}/login".format(self.url_prefix)
        aqua_credentials = json.dumps(dict(id=self.id, password=password, remember=self.remember))
        response = requests.post(url, data=aqua_credentials, verify=self.verify_tls, headers=self.headers,
                                 proxies=self.proxy)
        response_json = json.loads(response.content.decode('utf-8'))

        if 'token' in response_json:
            self.token = response_json['token']
        else:
            print(response_json['message'])
            raise Exception("Authentication Error")

        self.role = response_json['user']['role']
        self.is_super = response_json['user']['is_super']
        self.headers['Authorization'] = f"Bearer {self.token}"
        return 'Authentication successful'

    # Send the API request
    """
    Send the API request
    """

    def send_request(self, url, method='get', data=None):
        request_method = getattr(requests, method)

        try:
            response = request_method(url=url, data=data, verify=self.verify_tls, headers=self.headers,
                                      proxies=self.proxy)
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                if content != '':
                    content = json.loads(content)
                else:
                    content = json.loads('{}')

                return content
            elif response.status_code == 204 or response.status_code == 201:
                return json.loads('{}')
            else:
                return json.loads(response.content)

        except Exception as e:
            print(e)

    # Consoles
    def consoles(self):
        """
        Retrieve the configured consoles information

        :return: Produces a JSON array of all consoles configured in the system
        """
        url = "{}/consoles".format(self.url_prefix)
        return self.send_request(url)

    def servers(self):
        url = "{}/servers".format(self.url_prefix)
        return self.send_request(url)

    # Infrastructure
    def list_assets(self, page: str = 1, page_size: str = 50, type: str = None, search: str = None):
        """
        Retrieve details of hosts and clusters configured in system.

        :param page: list from provided page of results
        :param page_size: list at most the provided number
        :param type: node or cluster
        :return: list of nodes and clusters
        """
        query_string = urlencode({k: v for (k, v) in locals().items() if
                                  v is not None and k is not 'self'})  # build query string from parameters that are not None
        url = "{}/infrastructure?{}".format(self.url_prefix.replace('v1', 'v2'), query_string)
        return self.send_request(url)

    def get_asset_details_by_id(self, id: str = 1):
        """
        Retrieve details of identified host or cluster in system by id.

        :param id: host or cluster id
        :return: details of asset
        """
        url = "{}/infrastructure/{}".format(self.url_prefix.replace('v1', 'v2'), id)
        return self.send_request(url)

    # Inventory
    def inventory_scopes(self):
        url = "{}/inventory/scopes".format(self.url_prefix.replace('v1', 'v2'))
        return self.send_request(url)

    # Registries
    def list_registries(self):
        url = "{}/registries".format(self.url_prefix)
        return self.send_request(url)

    def create_image_registry(self, reg_type: str, name: str, description: str, username: str, password: str,
                              url: str = None, prefixes: str = None, auto_pull: bool = False):
        """
        Create a new image registry

        :param reg_type: the type of the registry. i.e HUB (Docker Hub), AWS, GCR, ENGINE (direct connect to docker engine), V1/V2 (General Docker registries)
        :param name: the name of the registry; string, required - this will be treated as the registry's ID, so choose a simple alphanumerical name without special signs and spaces
        :param description:
        :param username: the username for registry authentication; string, optional
        :param password: the password for registry authentication; string, optional
        :param url: the URL, address or region of the registry; string, optional
        :param prefixes: See https://docs.aquasec.com/reference#section-image-registry-prefixes
        :param auto_pull: whether to automatically pull images from the registry on creation and daily; boolean, defaults to false

        :return: If successful, a 204 No Content response will be returned. Note that if auto_pull is enabled, the server
                 will immediately begin pulling images from the registry.
        """
        api_url = "{}/registries".format(self.url_prefix)
        data = json.dumps(
            dict(type=reg_type, name=name, description=description, username=username, password=password, url=url,
                 prefixes=prefixes, auto_pull=auto_pull))
        return self.send_request(api_url, method='post', data=data)

    def image_registry(self, name: str):
        url = "{}/registries/{}".format(self.url_prefix, name)
        return self.send_request(url)

    def delete_registry(self, name: str):
        """
        Remove an existing image registry

        :param name: registry friendly name within Aqua
        :return: Upon successful removal, a 204 No Content response will be returned
        """
        url = "{}/registries/{}".format(self.url_prefix, name)
        return self.send_request(url, method='delete')

    # Image Profiles
    def list_profiles(self):
        """
        Lists of all image runtime profiles in the system

        :return: a list of all image runtime profiles in the system
        """
        url = "{}/securityprofiles".format(self.url_prefix)
        response = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return json.loads(response.content.decode('utf-8'))

    def end_profiling_session(self, registry_name: str, repository: str):
        """
        End a profiling session
        There are two ways to end the profiling session: stopping the containers that were started in the previous stage,
        or issuing an API call. Using the API call will cause the server to cease monitoring the containers' activity,
        but the containers will continue to live, so only use it if you still need them.

        :param registry_name:
        :param repository:
        :return: If the session is successfully terminated, an empty successful response is returned.
        """
        url = "{}/profiler_sessions/{}/{}/stop_containers".format(self.url_prefix, registry_name, repository)
        response = requests.post(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return response.content.decode('utf-8')

    def get_suggested_profile(self, registry_name: str, repository: str):
        """
        Get suggested profile generated in a profiling session

        :param registry_name:
        :param repository:
        :return: the suggested image runtime profile in the standard image runtime profile structure.
        """
        url = "{}/profiler_sessions/{}/{}/advice".format(self.url_prefix, registry_name, repository)
        response = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return json.loads(response.content.decode('utf-8'))

    def create_profile(self, profile: str):
        """
        Create a new image runtime profile

        :param profile: json object i.e. returned from get_suggested_profile
        :return: A successful creation of the new profile will result in a 204 No Content response.
        """
        url = "{}/securityprofiles".format(self.url_prefix)
        response = requests.post(url, data=profile, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return response

    def attach_profile(self, registry_name: str, repository: str, policy_name: str):
        """
        Attach an image runtime profile to a repository

        :param registry_name:
        :param repository:
        :param policy_name:
        :return:  Upon success, this route will return a 204 No Content response.
        """
        url = "{}/registry/{}/repos/{}/policy/{}".format(self.url_prefix, registry_name, repository, policy_name)
        # response = requests.put(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        # return response
        return self.send_request(url, 'put')

    def get_profile(self, profile_name: str):
        """
        Return the structure of an image runtime profile

        :param profile_name: name of profile to retrieve
        :return: the structure of an image runtime profile
        """
        url = "{}/securityprofiles/{}".format(self.url_prefix, profile_name)
        return self.send_request(url)

    def modify_profile(self, profile_name: str, profile: str):
        """
        Update an existing image runtime profile

        :param profile_name: name of profile to update
        :param profile: json object i.e. returned from get_suggested_profile
        :return: A successful creation of the new profile will result in a 204 No Content response.
        """
        url = "{}/securityprofiles/{}".format(self.url_prefix, profile_name)
        response = requests.put(url, data=profile, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return response

    # image export and import
    def export_images(self, images: List[str]):
        url = "{}/images/export".format(self.url_prefix)
        response = requests.post(url, data=json.dumps(dict(images=images)), verify=self.verify_tls,
                                 headers=self.headers, proxies=self.proxy)
        return response.json()

    # scanning images

    def scan_status(self, registry_name: str, image_name: str, image_tag: str = 'latest') -> Dict:
        """Get status of an image vulnerability scan.

        :param registry_name: name of the registry
        :param image_name: name of container image
        :param image_tag: optional. image tag. defaults to latest
        :return: scan status results as Dict
        """
        url = "{}/scanner/registry/{}/image/{}:{}/status".format(self.url_prefix, registry_name, image_name, image_tag)
        return self.send_request(url)

    def scan_results(self, registry_name: str, image_name: str, image_tag: str = 'latest'):
        url = "{}/scanner/registry/{}/image/{}:{}/scan_result".format(self.url_prefix, registry_name, image_name,
                                                                      image_tag)
        return self.send_request(url)

    def scan_queue(self):
        url = "{}/scanqueue/summary".format(self.url_prefix)
        return self.send_request(url)

    def start_image_scan(self, registry_name: str, image_name: str, image_tag: str = 'latest') -> Dict:
        """Get status of an image vulnerability scan.

        :param registry_name: name of the registry
        :param image_name: name of container image
        :param image_tag: optional. image tag. defaults to latest
        :return: scan status as Dict
        """
        url = "{}/scanner/registry/{}/image/{}:{}/scan".format(self.url_prefix, registry_name, image_name, image_tag)
        return self.send_request(url=url, method='post')

    """
    Services
    """

    def list_services(self):
        """
        Returns a list of all Aqua services in the system

        :return: Return structure is a JSON array of service objects
        """
        url = f"{self.url_prefix}/applications"
        return self.send_request(url=url)

    # secrets
    """
    Secrets
    """

    def list_secrets(self):
        url = "{}/secrets".format(self.url_prefix)
        return self.send_request(url)

    def get_secret(self, secret_name: str):
        url = "{}/secrets/{}".format(self.url_prefix, secret_name)
        return self.send_request(url)

    """
    Secret Key Stores
    """

    def list_secret_keystores(self):
        """
        List all existing secret key stores

        :return: If successful, a 200 OK response status returned.
                 A JSON list of all existing secret key stores will be returned
        """
        url = "{}/settings/keystores".format(self.url_prefix)
        return self.send_request(url)

    def create_secret_keystore(self, name: str, url: str, token: str, user: str, type: str = 'vault',
                               enabled: bool = True):
        """
        This method expects the request structure described at https://docs.aquasec.com/reference#section-secret-key-store-structure

        :param name: reference name of the secret key store to create; string, required
        :param url: for vault type this is the URL of the vault service, for KMS this is the access ID; string; required only for vault type
        :param token: the vault token, and for KMS, this is the secret key; string, required only for vault type
        :param user: for vault this is the secret back-end, for KMS this is the region; string, required
        :param type: the type of the secret key store; string, required [vault, kms]
        :param enabled: true when the secret key store is enabled; boolean

        :return: If successful, a {} will be returned
        """
        params = [(k, v) for (k, v) in locals().items() if v is not None and k is not 'self']
        data = json.dumps(dict(params))
        url = f"{self.url_prefix}/settings/keystores"
        return self.send_request(url, data=data, method='post')

    def delete_secret_keystore(self, name: str):
        """
        Deletes a secret key store

        :param name: the reference name of the secret key store.
        :return: If successful, a {}  will be returned.
        """
        url = f"{self.url_prefix}/settings/keystores/{name}"
        return self.send_request(url, method='delete')

    # enforcers
    """
    Enforcer Host Management
    """

    def hosts(self):
        """
        Get list of all Enforcers (hosts) on the Aqua Server

        :return: The response format will be a JSON array of enforcer structures. See enforcer structure for description.
                 https://docs.aquasec.com/reference#section-enforcer-structure
        """
        url = "{}/hosts".format(self.url_prefix)
        return self.send_request(url=url, method='get')

    """
    Containers
    """

    def containers(self, node_id: str = None, group_by: str = 'containers', status: str = 'running', page: str = '1',
                   pagesize: str = '50'):
        query_string = urlencode({k: v for (k, v) in locals().items() if v is not None and k is not 'self'})
        url = f"{self.url_prefix}/containers?{query_string}"
        return self.send_request(url=url, method='get')

    def create_enforcer_group(self, type, id, logicalname, host_os, service_account, namespace, runtime, token,
                              enforcer_image, enforce, gateways, orchestrator, runtime_options):
        """Create an enforcer group.

        :param type: which enforcer (agent, micro-enforcer, nano-enforcer, vm-enforcer)
        :param id: name of the enforcer group
        :param logicalname: prefix for the enforcer names
        :param host_os: Linux or Windows
        :param service_account: Kubernetes service account
        :param namespace: Namespace Aqua deployed too
        :param runtime: docker, crio, containerd
        :param token: Installation token to identify group
        :param enforcer_image: image to pull and deploy
        :param enforce: bool - audit = False, enforce = True
        :param gateways: string array of gateways
        :param orchestrator: type of orchestrator (docker, kubernetes, openshift, pas)
        :param runtime_options: map of policy options
        :return: A successful creation of the new enforcer group will result in a json response with the profile
        """
        url = "{}/hostsbatch".format(self.url_prefix)
        data = json.dumps(
            dict(id=id, hostname=logicalname, logicalname=logicalname, host_os=host_os, service_account=service_account,
                 namespace=namespace, runtime_type=runtime, \
                 token=token, enforcer_image=enforcer_image, enforce=enforce, gateways=gateways,
                 orchestrator={"type": orchestrator, "service_account": service_account, \
                               "namespace": namespace, "project": namespace},
                 audit_failed_login=runtime_options["audit_failed_login"],
                 audit_success_login=runtime_options["audit_success_login"], \
                 container_activity_protection=runtime_options["container_activity_protection"],
                 network_protection=runtime_options["network_protection"],
                 sync_host_images=runtime_options["sync_host_images"], \
                 syscall_enabled=runtime_options["syscall_enabled"],
                 user_access_control=runtime_options["user_access_control"],
                 risk_explorer_auto_discovery=runtime_options["risk_explorer_auto_discovery"], \
                 host_protection=runtime_options["host_protection"],
                 host_network_protection=runtime_options["host_network_protection"],
                 image_assurance=runtime_options["image_assurance"]))
        return self.send_request(url, method='post', data=data)

    def enforcer_details(self, id: str):
        """
         Get Enforcer details

        :param id: host/enforcer id
        :return:  The return structure is described in Enforcer Structure. https://docs.aquasec.com/reference#section-enforcer-structure
        """
        url = "{}/hosts/{}".format(self.url_prefix, id)
        return self.send_request(url)

    def list_batch_install_tokens(self):
        """
        List batch install tokens
        :return:Successful response will include a JSON array of objects. https://docs.aquasec.com/reference#section--list-batch-install-tokens-
        """
        url = f"{self.url_prefix}/hostsbatch"
        return self.send_request(url)

    # dashboard
    """
    Dashboard

    :param: registry: local name for configured registry
    :param: hosts: filter data by node(s)
    :param: containers_app: this represents a service that is configured
    :return: A json payload containing the severity information totals for Running Containers, Images and Vulnerabilities as well as Alert and Audit tickers
    """

    def dashboard(self, registry: str, hosts: str, containers_app: str):
        query_string = urlencode({k: v for (k, v) in locals().items() if v is not None and k is not 'self'})
        url = f"{self.url_prefix}/dashboard?{query_string}"
        return self.send_request(url=url, method='get')

    """
    Trends

    :param: trend: What type of trend to retrieve, options are: containers, images, vulnerabilities
    :return: A json payload containing the trend numbers based on epoch timestamp
    """

    def trends(self, trend: str):
        url = f"{self.url_prefix}/dashboard/{trend}/trends"
        return self.send_request(url=url, method='get')

    def export_settings(self, settings: List = None, key: str = None):
        """
        export settings and policies

        :param settings: list of string representing settings to export. default is all settings
        :param key: 32-character key if default key not to be used
        :return: settings dict
        """
        if key is None:
            url = f"{self.url_prefix}/settings/export"
        else:
            url = f"{self.url_prefix}/settings/export?encryption_key={key}"

        if settings is None:
            settings = ["registries", "settings", "policy.images_assurance", "policy.runtime_profile",
                        "policy.user_access_control", \
                        "policy.container_firewall", "policy.runtime_policies", "images", "labels", "secrets",
                        "applications"]
        return self.send_request(url=url, method='post', data=json.dumps(settings))

    def import_settings(self, settings: Dict, key: str = None):
        """
        import settings and policies

        :param settings: dict representing aqua settings
        :param key: 32-character key if default key not to be used
        :return: {} if successful
        """
        if key is None:
            url = f"{self.url_prefix}/settings/import"
        else:
            url = f"{self.url_prefix}/settings/import?encryption_key={key}"

        return self.send_request(url=url, method='post', data=json.dumps(settings))

    """
    v2 calls
    """

    """
    v2 Images
    """

    def register_image(self, registry, image_name, image_tag: str = 'latest'):
        url = "{}/images".format(self.url_prefix.replace('v1', 'v2'))
        data = json.dumps(dict(registry=registry, image=f'{image_name}:{image_tag}'))
        # resp = requests.post(url, data=data, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return self.send_request(url=url, method='post', data=data)

    def list_registered_images(self, registry: str = None, repository: str = None, name: str = None, page: int = None,
                               page_size: int = None, order_by: str = None):
        query_string = urlencode({k: v for (k, v) in locals().items() if
                                  v is not None and k is not 'self'})  # build query string from parameters that are not None
        url = "{}/images?{}".format(self.url_prefix.replace('v1', 'v2'), query_string)
        resp = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()

    def get_registered_images(self, registry: str = None, repository: str = None, name: str = None):
        query_string = urlencode({k: v for (k, v) in locals().items() if
                                  v is not None and k is not 'self'})  # build query string from parameters that are not None
        url = "{}/images?{}".format(self.url_prefix.replace('v1', 'v2'), query_string)
        resp = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()

    def get_registered_image(self, registry: str, repo: str, tag: str = "latest"):
        url = "{}/images/{}/{}/{}".format(self.url_prefix.replace('v1', 'v2'), registry, repo, tag)
        resp = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()

    def list_image_vulnerabilities(self, registry, image_name, image_tag: str = 'latest', page: int = 0, pagesize: int = 50,
                                   show_negligible: bool = True, hide_base_image: bool = False):
        query_string = urlencode({k: v for (k, v) in locals().items() if v is not None and k not in ['self', 'image_tag']})
        url = "{}/images/{}/{}/{}/vulnerabilities?{}".format(self.url_prefix.replace('v1', 'v2'), registry, image_name,
                                                             image_tag, query_string)
        return self.send_request(url)

    def risks_image_vulnerabilities(self, registry, image_name, image_tag: str = 'latest', page: int = 0, pagesize: int = 50,
                                   include_vpatch_info: str = 'true',show_negligible: str = 'true', hide_base_image: str = 'false'):
        image_name = f"{image_name}:{image_tag}"
        query_string = urlencode({k: v for (k, v) in locals().items() if v is not None and k not in ['self', 'image_tag']})
        url = "{}/risks/vulnerabilities?{}".format(self.url_prefix.replace('v1', 'v2'), query_string)
        return self.send_request(url)

    def heuristics(self, registry: str, image_name:str, image_tag: str, cve: str, resource_name: str, resource_type: str):
        full_image_name = f"{image_name}:{image_tag}"
        locals()['repo_name'] = image_name
        image_name = f"{image_name}:{image_tag}"
        query_string = urlencode({k: v for (k, v) in locals().items() if v is not None and k not in ['self', 'image_tag']})
        url = "{}/heuristics?{}".format(self.url_prefix.replace('v1', 'v2'), query_string)


    def list_image_malware(self, registry: str, repo: str, tag: str = "latest"):
        url = "{}/images/{}/{}/{}/malware".format(self.url_prefix.replace('v1', 'v2'), registry, repo, tag)
        return self.send_request(url)

    def list_image_sensitive_data(self, registry: str, repo: str, tag: str = "latest"):
        url = "{}/images/{}/{}/{}/sensitive".format(self.url_prefix.replace('v1', 'v2'), registry, repo, tag)
        return self.send_request(url)

    def list_image_layers(self, registry: str, repo: str, tag: str = "latest"):
        url = "{}/images/{}/{}/{}/history_layers".format(self.url_prefix.replace('v1', 'v2'), registry, repo, tag)
        return self.send_request(url)

    def scan_history(self, registry: str, repo: str, tag: str = 'latest', order_by: str = '-date'):
        """
        Retrieve scan history for a container image

        :param registry: name of the registry
        :param repo: name of the repo
        :param tag: image tag
        :param order_by: date (ASC) or -date (DESC)
        :return: scan history object
        """
        url = "{}/images/{}/{}/{}/scan_history?order_by={}".format(self.url_prefix.replace('v1', 'v2'), registry, repo,
                                                                   tag, order_by)
        return self.send_request(url)

    def notifications(self):
        """
        Get information of the last notification sent by the environment

        :return: notifications as dict
        """
        url = "{}/notifications".format(self.url_prefix.replace('v1', 'v2'))
        return self.send_request(url)

    def licenses(self):
        url = "{}/licenses".format(self.url_prefix.replace('v1', 'v2'))
        return self.send_request(url)

    def license(self, id: str):
        url = "{}/licenses?id={}".format(self.url_prefix.replace('v1', 'v2'), id)
        return self.send_request(url)


    def list_image_assurance(self):
        """
        Lists of all image assurance policies in the system

        :return: a list of all assurance policies in a json
        """
        url = "{}/assurance_policy".format(self.url_prefix.replace('v1', 'v2'))
        response = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return json.loads(response.content.decode('utf-8'))   

    def get_image_assurance(self, policy_name: str, policy_type: str):
        """
        Return the structure of an image runtime profile

        :param profile_name: name of profile to retrieve
        :param policy_type: the type of assurance policy (image | host | function | cf_application)
        :return: the structure of an image runtime profile

        NOTE: 
        """
        url = "{}/assurance_policy/{}/{}".format(self.url_prefix.replace('v1', 'v2'),policy_type, policy_name)
        response = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return json.loads(response.content.decode('utf-8'))   

    def modify_image_assurance(self, policy_name: str, policy_file: str, policy_type: str):
        """
        Update an existing image assurance policy

        :param policy_name: name of policy to update
        :param policy_file: json object i.e. returned from list_image_assurance or get_image_assurance
        :param policy_type: the type of assurance policy (image | host | function | cf_application)
        :return: A successful creation of the new profile will result in a 204 No Content response.
        """
        url = "{}/assurance_policy/{}/{}".format(self.url_prefix.replace('v1', 'v2'),policy_type, policy_name)
        response = requests.put(url, data=str(policy_file), verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return response

######################################################################
#  the retrieval and modification of runtime policies
######################################################################
    def list_runtime_policies(self):
        """
        Lists of all runtime policies in the system

        :return: a list of all runtime policies in a json
        """
        url = "{}/runtime_policies".format(self.url_prefix.replace('v1', 'v2'))
        response = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return json.loads(response.content.decode('utf-8'))   

    def get_runtime_policies(self, policy_name: str):
        """
        Return the structure of a runtime policy

        :param profile_name: name of policy to retrieve
        :return: the structure of a runtime policy
        """
        url = "{}/runtime_policies/{}".format(self.url_prefix.replace('v1', 'v2'), policy_name)
        return self.send_request(url)

    def modify_runtime_policies(self, policy_name: str, policy_file: str):
        """
        Update an existing image assurance policy

        :param policy_name: name of policy to update
        :param policy_file: json object i.e. returned from list_runtime_policies or get_runtime_policies
        :return: A successful creation of the new policy will result in a 204 No Content response.
        """
        url = "{}/runtime_policies/{}".format(self.url_prefix.replace('v1', 'v2'), policy_name)
        response = requests.put(url, data=policy_file, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return response

