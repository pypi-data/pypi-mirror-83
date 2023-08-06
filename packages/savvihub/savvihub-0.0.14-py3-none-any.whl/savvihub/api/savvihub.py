import requests
import typing

from savvihub.api.types import PaginatedMixin, SavviHubListResponse, SavviHubFileObject, SavviHubDataset, \
    SavviHubKernelResource, SavviHubKernelImage, SavviHubExperiment, SavviHubProject, SavviHubWorkspace, SavviHubUser, \
    SavviHubExperimentLog
from savvihub.common.constants import API_HOST


class SavviHubClient:
    def __init__(self, *, session=requests.Session(), token=None, url=API_HOST, content_type='application/json'):
        self.session = session
        self.url = url
        self.token = token
        
        session.headers = {'content-type': content_type}
        if token:
            session.headers['authorization'] = 'Token %s' % token

    def get(self, url, params=None, raise_error=False, **kwargs):
        r = self.session.get(f'{self.url}{url}', params=params, **kwargs)
        if raise_error:
            r.raise_for_status()
        return r

    def get_all(self, url, params=None, raise_error=False, **kwargs):
        raw_resp = self.get(url, params=params, raise_error=raise_error, **kwargs)
        resp = PaginatedMixin(raw_resp.json())
        results = []

        fetched_items = 0
        while True:
            fetched_items += len(resp.results)
            results.extend(resp.results)
            if fetched_items >= resp.total:
                break
            raw_resp = self.get(url, params={**params, 'after': resp.endCursor}, raise_error=raise_error, **kwargs)
            resp = PaginatedMixin(raw_resp.json())
        return results

    def get_all_without_pagination(self, url, params=None, raise_error=False, **kwargs):
        raw_resp = self.get(url, params=params, raise_error=raise_error, **kwargs)
        resp = SavviHubListResponse(raw_resp.json())
        return resp.results

    def post(self, url, data, raise_error=False, **kwargs):
        r = self.session.post(f'{self.url}{url}', json=data, **kwargs)
        if raise_error:
            r.raise_for_status()
        return r

    def delete(self, url, raise_error=False, **kwargs):
        r = self.session.delete(f'{self.url}{url}', **kwargs)
        if raise_error:
            r.raise_for_status()
        return r

    def patch(self, url, data, raise_error=False, **kwargs):
        r = self.session.patch(f'{self.url}{url}', json=data, **kwargs)
        if raise_error:
            r.raise_for_status()
        return r

    def get_my_info(self):
        r = self.get(f'/v1/api/accounts/me/')
        if r.status_code != 200:
            return None
        return SavviHubUser(r.json())

    def volume_file_list(self, volume_id, *, prefix='', **kwargs) -> typing.List[SavviHubFileObject]:
        r = self.get(f'/v1/api/volumes/{volume_id}/files/', params={'prefix': prefix, 'get_all': 'true'}, **kwargs)
        return [SavviHubFileObject(x) for x in r.json().get('results')]

    def volume_file_create(self, volume_id, path, is_dir, **kwargs):
        return self.post(f'/v1/api/volumes/{volume_id}/files/', {
            'path': path,
            'is_dir': is_dir
        }, **kwargs)

    def volume_file_uploaded(self, volume_id, path, is_dir, **kwargs):
        return self.post(f'/v1/api/volumes/{volume_id}/files/uploaded/', {
            'path': path,
        }, **kwargs)

    def experiment_read(self, **kwargs) -> SavviHubExperiment:
        return SavviHubExperiment(self.get(f'/v1/api/experiments/', **kwargs).json())

    def experiment_list(self, workspace, project, **kwargs):
        return [SavviHubExperiment(x) for x in self.get_all_without_pagination(f'/v1/api/workspaces/{workspace}/projects/{project}/experiments/?orderby.direction=DESC', **kwargs)]

    def experiment_log(self, workspace, project, experiment_number, **kwargs):
        return [SavviHubExperimentLog(x) for x in self.get(f'/v1/api/workspaces/{workspace}/projects/{project}/experiments/{experiment_number}/log/', **kwargs).json().get('logs')]

    def experiment_create(self, workspace, project, image_id, resource_spec_id, branch, dataset_mount_infos, start_command, **kwargs):
        return self.post(f'/v1/api/workspaces/{workspace}/projects/{project}/experiments/', {
            'image_id': image_id,
            'resource_spec_id': resource_spec_id,
            'branch': branch,
            'dataset_mount_infos': dataset_mount_infos,
            'start_command': start_command,
        }, **kwargs)

    def experiment_progress_update(self, experiment_id, row, **kwargs):
        return self.post(f'/v1/api/experiments/{experiment_id}/progress/', {
            'metrics': [row],
        }, **kwargs)

    def kernel_image_list(self, workspace):
        results = self.get_all_without_pagination(f'/v1/api/workspaces/{workspace}/kernels/images/')
        return [SavviHubKernelImage(x) for x in results]

    def kernel_resource_list(self, workspace):
        results = self.get_all_without_pagination(f'/v1/api/workspaces/{workspace}/kernels/resource_specs')
        return [SavviHubKernelResource(x) for x in results]

    def workspace_read(self, workspace):
        resp = self.get(f'/v1/api/workspaces/{workspace}/')
        if resp.status_code == 404:
            return None
        elif resp.status_code != 200:
            resp.raise_for_status()
        return SavviHubWorkspace(resp.json())

    def project_read(self, workspace, project):
        resp = self.get(f'/v1/api/workspaces/{workspace}/projects/{project}/')
        if resp.status_code == 404:
            return None
        elif resp.status_code != 200:
            resp.raise_for_status()
        return SavviHubProject(resp.json())

    def project_github_create(self, workspace, project, github_owner, github_repo, **kwargs):
        return SavviHubProject(self.post(f'/v1/api/workspaces/{workspace}/projects_github/', {
            'slug': project,
            'github_owner': github_owner,
            'github_repo': github_repo,
        }, **kwargs).json())

    def public_dataset_list(self):
        results = self.get_all(f'/v1/api/datasets/public/')
        return [SavviHubDataset(x) for x in results]

    def dataset_list(self, workspace):
        results = self.get_all(f'/v1/api/workspaces/{workspace}/datasets/')
        if not results:
            return []
        return [SavviHubDataset(x) for x in results]

    def dataset_read(self, workspace, dataset, **kwargs):
        return SavviHubDataset(self.get(f'/v1/api/workspaces/{workspace}/datasets/{dataset}/', **kwargs).json())

    def dataset_snapshot_file_list(self, workspace, dataset, ref, **kwargs):
        r = self.get(f'/v1/api/workspaces/{workspace}/datasets/{dataset}/snapshots/{ref}/files/', **kwargs)
        return [SavviHubFileObject(x) for x in r.json().results]
