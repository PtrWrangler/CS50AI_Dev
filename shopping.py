import csv
from select import select
import sys
from time import monotonic
from numpy import true_divide
from sklearn.linear_model import Perceptron

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    evidence                = []
    labels                  = []

    #Read all the CSV data into a dict, then create our desired evidence list of lists, and labels list
    with open(filename, newline='') as csv_file:
        csv_dict = csv.DictReader(csv_file)      
    
        for col in csv_dict:
            evidence_row = []
            evidence_row.append( int(col['Administrative']) )
            evidence_row.append( float(col['Administrative_Duration']) )
            evidence_row.append( int(col['Informational']) )
            evidence_row.append( float(col['Informational_Duration']) )
            evidence_row.append( int(col['ProductRelated']) )
            evidence_row.append( float(col['ProductRelated_Duration']) )
            evidence_row.append( float(col['BounceRates']) )
            evidence_row.append( float(col['ExitRates']) )
            evidence_row.append( float(col['PageValues']) )
            evidence_row.append( float(col['SpecialDay']) )
            evidence_row.append( process_month(col['Month']) )
            evidence_row.append( int(col['OperatingSystems']) )
            evidence_row.append( int(col['Browser']) )
            evidence_row.append( int(col['Region']) )
            evidence_row.append( int(col['TrafficType']) )
            evidence_row.append( 1 if col['VisitorType'] == 'Returning_Visitor' else 0 )
            evidence_row.append( 1 if col['Weekend'] == 'TRUE' else 0 )
            
            evidence.append(evidence_row)

            labels.append( 1 if col['Revenue'] == 'TRUE' else 0 )

    return (evidence, labels)

def process_month(str_month):
    return {
        'Jan' : 0,
        'Feb' : 1,
        'Mar' : 2,
        'Apr' : 3,
        'May' : 4,
        'June': 5,
        'Jul' : 6,
        'Aug' : 7,
        'Sep' : 8,
        'Oct' : 9,
        'Nov' : 10,
        'Dec' : 11
    }.get(str_month, 0)
     


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    # Use KNeighborsClassifier model, fit the model with our data from the input csv
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # compare all of the actual labels to the predicted labels and accumulate the true positive/negative results
    true_positives = 0
    true_negatives = 0
    total = 0
    for actual, predicted in zip(labels, predictions):
        total += 1
        if actual == predicted and actual == 1:
            true_positives += 1
        elif actual == predicted and actual == 0:
            true_negatives += 1

    print ("True Positives: " + str(true_positives) + ", True Negatives:" + str(true_negatives) + ", Total results:" + str(total))

    # Calculate the rate of these True Positives/Negatives as Sensitivity/Specificity
    sensitivity = true_positives / total
    specificity = true_negatives / total

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
