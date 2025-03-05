n_iterations = 2
inputs = {"topic": "CrewAI Training"}
filename = "your_model.pkl"

try:
    YourCrewName_Crew().crew().train(
      n_iterations=n_iterations, 
      inputs=inputs, 
      filename=filename
    )

except Exception as e:
    raise Exception(f"An error occurred while training the crew: {e}")
