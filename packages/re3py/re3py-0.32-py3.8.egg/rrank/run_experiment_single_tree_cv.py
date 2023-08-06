from core import DecisionTree
from heuristic import *
from data import Dataset
from evaluation import Accuracy
from cross_validation import create_folds
import sys
import itertools

print("Starting experiment")

fold = int(sys.argv[1])

minimal_examples_in_leaf = 'minimal_examples_in_leaf'
minimal_impurity = "minimal_impurity"

descriptive = 'relations_descriptive.txt'
target = "relation_target.txt"
s_file = 'settings.s'
s = Settings(s_file)
d = Dataset(s_file, descriptive, target)
tree_params = {'heuristic': HeuristicGini(),
               'max_number_atom_tests': 2,
               'allowed_atom_tests': s.get_atom_tests_structured(),
               'allowed_aggregators': s.get_aggregates(),
               'java_port': None,
               'only_existential': True
               }

target_values = list({element.get_target() for element in d.get_target_data()})
a_train_test = [Accuracy(target_values), Accuracy(target_values)]

dataset_folds = list(create_folds(d, folds_file="folds.txt"))
train_set, test_set = dataset_folds[fold]

IMPURITIES = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2]
LEAF_SIZES = [1, 5, 10, 15, 20]

for impurity, leaf in itertools.product(IMPURITIES, LEAF_SIZES):
    print("Building the tree with impurity and leaf", impurity, leaf)
    tree_params[minimal_impurity] = impurity
    tree_params[minimal_examples_in_leaf] = leaf

    learner = DecisionTree(**tree_params)

    learner.build(train_set)
    learner.print_model('experiment_impurity{}_leaf{}.txt'.format(impurity, leaf))

    true_values_train = [e.get_target() for e in train_set.get_target_data()]
    true_values_test = [e.get_target() for e in test_set.get_target_data()]

    true = [true_values_train, true_values_test]
    predicted_values_train = [learner.predict(e) for e in train_set.get_target_data()]
    predicted_values_test = [learner.predict(e) for e in test_set.get_target_data()]
    predicted = [predicted_values_train, predicted_values_test]
    for a, t, p in zip(a_train_test, true, predicted):
        a.add_many(t, p)

    with open("experiment_impurity{}_leaf{}.log".format(impurity, leaf), "w") as f:
        for name, a in zip(["train", "test"], a_train_test):
            print(name, file=f)
            a.evaluate()
            print(a.measure_value, file=f)
            print(a.class_indices, file=f)
            print(a.confusion_matrix, file=f)
