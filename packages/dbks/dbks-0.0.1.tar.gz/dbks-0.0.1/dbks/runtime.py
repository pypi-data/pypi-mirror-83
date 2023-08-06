class Runtime:
    @staticmethod
    def v3(major: str, feature: str, ml_type: str = None, scala_version: str = "2.12"):
        if ml_type and ml_type.lower() not in ["cpu", "gpu"]:
            raise ValueError('"ml_type" can only be "cpu" or "gpu"!')
        return "".join(
            [
                f"{major}.",
                f"{feature}.x",
                "" if not ml_type else f"-{ml_type}-ml",
                f"-scala{scala_version}",
            ]
        )

    @staticmethod
    def v2(
        major: str,
        feature: str,
        maintenance: str,
        runtime_version: str,
        scala_version: str = "2.11",
    ):
        raise ValueError("This version of runtime is no longer supported!")

    @staticmethod
    def light(major: str, feature: str, scala_version: str = "2.11"):
        return f"apache-spark.{major}.{feature}.x-scala{scala_version}"
