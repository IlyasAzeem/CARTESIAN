import pandas as pd
from sklearn import preprocessing
import xgboost
import pickle

df_r = pd.read_csv("Output/pygithub.csv", sep=",", encoding="ISO-8859-1")

file_path = 'Output/results.csv'


# One hot encoding
def encode_labels(df1, column_name):
    encoder = preprocessing.LabelEncoder()
    df1[column_name] = [str(label) for label in df1[column_name]]
    encoder.fit(df1[column_name])
    one_hot_vector = encoder.transform(df1[column_name])
    return  one_hot_vector

predictors_a = ['Project_Age', 'Project_Accept_Rate', 'Language', 'Watchers', 'Stars', 'Team_Size', 'Additions_Per_Week',
                       'Deletions_Per_Week', 'Comments_Per_Merged_PR', 'Churn_Average', 'Close_Latency', 'Comments_Per_Closed_PR',
                       'Forks_Count', 'File_Touched_Average', 'Merge_Latency', 'Rebaseable', 'Additions', 'Deletions',
                       'Wait_Time', 'PR_Latency', 'Files_Changed', 'Label_Count', 'Workload', 'Commits_Average', 'Contributor',
                       'Followers', 'Closed_Num', 'Public_Repos', 'Accept_Num', 'User_Accept_Rate', 'Contributions', 'Closed_Num_Rate',
                       'Prev_PRs', 'Open_Issues', 'first_response', 'latency_after_first_response', 'X1_0', 'X1_1', 'X1_2',
                       'X1_3', 'X1_4', 'X1_5','X1_6', 'X1_7', 'X1_8', 'X1_9']
predictors_r = ['Project_Age', 'Project_Accept_Rate', 'Language', 'Watchers', 'Stars', 'Team_Size', 'Additions_Per_Week',
                     'Deletions_Per_Week', 'Comments_Per_Merged_PR', 'Contributor_Num', 'Churn_Average', 'Sunday', 'Monday',
                     'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Close_Latency', 'Comments_Per_Closed_PR',
                     'Forks_Count','File_Touched_Average', 'Merge_Latency', 'Rebaseable', 'Intra_Branch',
                     'Additions', 'Deletions', 'Day', 'Commits_PR', 'Wait_Time', 'Contain_Fix_Bug', 'PR_Latency', 'Files_Changed',
                     'Label_Count', 'Assignees_Count', 'Workload', 'PR_age', 'Commits_Average', 'Contributor', 'Followers',
                     'Closed_Num', 'Public_Repos', 'Organization_Core_Member', 'Accept_Num', 'User_Accept_Rate', 'Contributions',
                     'Closed_Num_Rate', 'Following', 'Prev_PRs', 'Review_Comments_Count', 'Participants_Count', 'Comments_Count',
                     'Last_Comment_Mention', 'Point_To_IssueOrPR', 'Open_Issues', 'first_response', 'latency_after_first_response',
                     'X1_0', 'X1_1', 'X1_2', 'X1_3', 'X1_4', 'X1_5', 'X1_6', 'X1_7', 'X1_8', 'X1_9']


def Cartesian_models(df_test_PR, file_path):
    pd.options.mode.chained_assignment = None
    df_r['Language'] = encode_labels(df_r, 'Language')

    with open('Models/accept_XGB_tool.pickle.dat', 'rb') as f:
        accept_model = pickle.load(f)
        # y_pred_accept = accept_model.predict(df_test_PR[predictors_a])
        y_pred_accept = accept_model.predict_proba(df_test_PR[predictors_a])[:,1]
        df_test_PR['Result_Accept'] = y_pred_accept

    with open('Models/response_XGB_tool.pickle.dat', 'rb') as f:
        response_model = pickle.load(f)
        # y_pred_response = response_model.predict(df_test_PR[predictors_r])
        y_pred_response = response_model.predict_proba(df_test_PR[predictors_r])[:,1]
        df_test_PR['Result_Response'] = y_pred_response

    df_test_PR['Score'] = (df_test_PR['Result_Accept'] + df_test_PR['Result_Response'])/2

    df_test_PR = df_test_PR.sort_values(by=['Score'], ascending=False)
    df_test_PR[['Pull_Request_ID', 'Title', 'url']].to_csv(file_path, sep=',', encoding='utf-8', index=False)




if __name__ == '__main__':


    """Calculate priority score for each project"""
    Cartesian_models(df_r, file_path)

