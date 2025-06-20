def clean_artifact_name(name: str) -> str:
    return os.path.splitext(name.strip().replace(" ", " "))[0]


df["clean_name"] = df["ARTIFACT_NAME"].apply(clean_artifact_name)


def get_artifact_info(self, artifact_name: str):
    clean_name = clean_artifact_name(artifact_name)
    return self.lookup.get(clean_name, (None, None))
