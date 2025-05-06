import pandas as pd

class ArtifactLookup:
    def __init__(self, csv_path: str):
        # Load CSV and index by Artifact_name for fast lookup
        self.df = pd.read_csv(csv_path, usecols=["Funding_Request_ID", "Division", "Artifact_name"])
        self.lookup = self.df.set_index("Artifact_name")[["Funding_Request_ID", "Division"]]

    def get_funding_info(self, artifact_name: str):
        try:
            result = self.lookup.loc[artifact_name]
            return result["Funding_Request_ID"], result["Division"]
        except KeyError:
            return None, None  # Not found

# Example usage:
# lookup = ArtifactLookup("data.csv")
# funding_id, division = lookup.get_funding_info("artifact_123")
