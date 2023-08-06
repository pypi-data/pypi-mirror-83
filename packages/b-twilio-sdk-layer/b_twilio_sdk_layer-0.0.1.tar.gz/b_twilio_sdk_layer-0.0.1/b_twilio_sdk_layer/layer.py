from functools import lru_cache
from typing import List

from aws_cdk.aws_lambda import Code, LayerVersion, Runtime
from aws_cdk.core import Stack, AssetHashType, BundlingOptions, BundlingDockerImage


class Layer(LayerVersion):
    def __init__(self, scope: Stack, name: str):
        self.__scope = scope

        super().__init__(
            scope=scope,
            id=name,
            code=Code.from_asset(
                self.get_source_path(),
                asset_hash_type=AssetHashType.BUNDLE,
                bundling=BundlingOptions(
                    image=BundlingDockerImage.from_registry('python:3.9'),
                    command=[
                        'bash', '-c',
                        (
                            'pip install -r requirements.txt -t /asset-output/python && '
                            'find /asset-output -type f -name "*.py[co]" -delete && '
                            'find /asset-output -type d -name "__pycache__" -delete'
                        )
                    ]
                )
            ),
            compatible_runtimes=self.runtimes(),
            layer_version_name=name,
        )

    @lru_cache
    def get_source_path(self) -> str:
        """
        Returns path to layer source.

        :return: Path to layer source.
        """
        from .source import root
        return root

    def runtimes(self) -> List[Runtime]:
        """
        Available runtimes for lambda functions.

        :return: List of available runtimes.
        """
        return [
            Runtime.PYTHON_2_7,
            Runtime.PYTHON_3_6,
            Runtime.PYTHON_3_7,
            Runtime.PYTHON_3_8
        ]
