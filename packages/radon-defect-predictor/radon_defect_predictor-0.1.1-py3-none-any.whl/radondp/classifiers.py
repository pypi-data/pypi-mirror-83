from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

classifiers_map = {
    'dt': DecisionTreeClassifier(),
    'nb': GaussianNB(),
    'logit': LogisticRegression(),
    'rf': RandomForestClassifier(),
    'svm': SVC()
}
