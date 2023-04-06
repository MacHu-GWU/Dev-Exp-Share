
import sagemaker
from sagemaker.sklearn import SKLearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression

from traceback import for
RandomForestRegressor().set_params(

)

model = SKLearn().deploy().delete_model()

model.fit()
model.deploy().delete_model()

sagemaker.Session().upload_data()