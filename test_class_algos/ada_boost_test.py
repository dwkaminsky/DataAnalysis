from sklearn.ensemble import AdaBoostClassifier
from config import base_path
from test_class_algos.fetch_data import get_test_df, split_into_test_train


def test_ada_model(df):
    X_TRAIN, Y_TRAIN, X_TEST, Y_TEST = split_into_test_train(df)
    clf = AdaBoostClassifier(n_estimators=100, random_state=0)
    clf.fit(X_TRAIN, Y_TRAIN)
    print(abs(clf.predict(X_TEST) - Y_TEST))


df = get_test_df()
print('Test Data Saved!')
df.to_csv(base_path() + '/data/test_data.csv')
test_ada_model(df)
