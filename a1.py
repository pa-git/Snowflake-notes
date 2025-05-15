class ArtifactLookup:
    def __init__(self, csv_path: str):
        # Load CSV with necessary columns
        df = pd.read_csv(csv_path, usecols=["Funding_Request_ID", "Division", "Artifact_name"])

        # Create a cleaned version of Artifact_name: strip and remove extension
        df["clean_name"] = df["Artifact_name"].apply(
            lambda name: os.path.splitext(name.strip())[0]
        )

        # Build a dictionary for fast lookup
        self.lookup = {
            row["clean_name"]: (row["Funding_Request_ID"], row["Division"])
            for _, row in df.iterrows()
        }

    def get_funding_info(self, artifact_name: str):
        # artifact_name is already clean (no extension, trimmed)
        return self.lookup.get(artifact_name, (None, None))
