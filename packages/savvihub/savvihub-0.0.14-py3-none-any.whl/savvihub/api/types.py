import inspect
import typeguard
import typing


class AnnotatedObject:
    def __init__(self, d: dict):
        resolved_types = {}
        for cls in self.__class__.mro():
            annotations = getattr(cls, '__annotations__', None)
            if annotations is None:
                continue

            for k, type_ in annotations.items():
                if k in resolved_types:
                    continue

                v = d.get(k, None)
                resolved_types[k] = type_

                if inspect.isclass(type_) and issubclass(type_, AnnotatedObject):
                    v = type_(v)
                else:
                    typeguard.check_type(k, v, type_)
                setattr(self, k, v)
        self.d = d

    def __str__(self):
        return f'[{self.__class__.__name__}] {self.d}'

    @property
    def dict(self):
        return self.d


class SavviHubFileObject(AnnotatedObject):
    class FileActionURL(AnnotatedObject):
        url: str

    path: str

    size: int
    hash: str

    download_url: FileActionURL
    upload_url: FileActionURL


class SavviHubKernelImage(AnnotatedObject):
    id: int
    image_url: str
    name: str


class SavviHubKernelResource(AnnotatedObject):
    id: int
    name: str
    cpu_limit: float
    mem_limit: str


class SavviHubDataset(AnnotatedObject):
    id: int
    slug: str
    main_volume_id: int


class SavviHubUser(AnnotatedObject):
    id: int
    github_authorized: bool


class SavviHubWorkspace(AnnotatedObject):
    id: int


class SavviHubProject(AnnotatedObject):
    id: int


class SavviHubExperiment(AnnotatedObject):
    id: int
    number: int
    status: str
    message: str
    output_volume_id: int


class SavviHubExperimentLog(AnnotatedObject):
    name: str
    stream: str
    message: str
    timestamp: float
    checksum: str


class SavviHubListResponse(AnnotatedObject):
    results: typing.List


class PaginatedMixin(AnnotatedObject):
    total: int
    startCursor: typing.Optional[str]
    endCursor: typing.Optional[str]
    results: typing.List
