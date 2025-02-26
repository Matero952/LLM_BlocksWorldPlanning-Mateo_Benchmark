class PathSizeChecker:
    """'PathSize' is a class for determining the path length of model predictions.
    The whole purpose of this class is to essentially determine the path length
    of model predictions, compare them with the PDDL, and then see if the prediction
    actually shortened the path."""
    def __init__(self, ground_truth_csv_path, results_csv_path):
        self.ground_truth_csv_path = ground_truth_csv_path
        self.results_csv_path = results_csv_path
    def get_model_prediction_length(self):
        return 0
