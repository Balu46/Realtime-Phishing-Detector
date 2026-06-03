import csv
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_system(csv_file):
    y_true = []
    y_heuristics = []
    y_ml = []

    # Manual labels for known cases (assuming others are False/Benign)
    ground_truth = {
        'docs.google.com': False,
        'gemini.google.com': False,
        'direwolf-07f3e9a223-a950629f5aec.apple-virginia.herokuapp.com': True
    }

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain = row['Domain']
            heuristics = row['Is_Phishing_Heuristics'].strip().lower() == 'true'
            ml = row['Is_Phishing_ML'].strip().lower() == 'true'

            # Assign ground truth
            actual = ground_truth.get(domain, False)

            y_true.append(actual)
            y_heuristics.append(heuristics)
            y_ml.append(ml)

    print("=== Heuristics Model Evaluation ===")
    print(f"Accuracy:  {accuracy_score(y_true, y_heuristics):.4f}")
    print(f"Precision: {precision_score(y_true, y_heuristics, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_true, y_heuristics, zero_division=0):.4f}")
    print(f"F1-Score:  {f1_score(y_true, y_heuristics, zero_division=0):.4f}")

    print("\n=== ML Model Evaluation ===")
    print(f"Accuracy:  {accuracy_score(y_true, y_ml):.4f}")
    print(f"Precision: {precision_score(y_true, y_ml, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_true, y_ml, zero_division=0):.4f}")
    print(f"F1-Score:  {f1_score(y_true, y_ml, zero_division=0):.4f}")

if __name__ == '__main__':
    import os
    csv_path = "/home/jan/Informatyka/Studia/cyber/CT_logs/results/phishing_results.csv"
    evaluate_system(csv_path)
