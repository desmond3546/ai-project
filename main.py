import pandas as pd # For Tabular Data Manipulation.
import matplotlib.pyplot as plt # For Basic Visualization
import seaborn as sns # For Interactive Visualization and it was made top of matplotlib itself.
import numpy as np # For numeric python
import matplotlib.pyplot as plt
plt.style.use("ggplot")
from sklearn.preprocessing import OrdinalEncoder
import warnings # For Ignoring Warnings
warnings.filterwarnings('ignore')
df = pd.read_csv("expanded_yield_df.csv")
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())
print(df.duplicated().sum())
print(df.shape)
plt.figure(figsize=(15,20))
sns.countplot(y = df['Area'])
plt.show()
plt.figure(figsize=(15,20))
sns.countplot(y = df['Item'])
plt.show()
country = df['Area'].unique()
yield_per_country = []
for state in country:
    yield_per_country.append(df[df['Area'] == state]['hg/ha_yield'].sum())

df['hg/ha_yield'].sum()
print(yield_per_country)
plt.figure(figsize=(15,20))
sns.barplot(y = country, x = yield_per_country)
plt.show()
crops = df['Item'].unique()
yield_per_crop = []
for crop in crops:
    yield_per_crop.append(df[df['Item'] == crop]['hg/ha_yield'].sum())

plt.figure(figsize=(15,20))
sns.barplot(y = crops, x = yield_per_crop)
plt.show()
print(df.columns)
col = ['Year', 'average_rain_fall_mm_per_year',
       'pesticides_tonnes', 'avg_temp', 'solar_radiation',
       'soil_organic_matter', 'soil_nitrogen', 'soil_phosphorus',
       'soil_potassium', 'Area', 'Item', 'hg/ha_yield']
df = df[col]
print(df.head())
X = df.drop('hg/ha_yield', axis = 1)
y = df['hg/ha_yield']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state = 0, shuffle=True)

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

ohe = OneHotEncoder(drop = 'first')
scale = StandardScaler()

preprocesser = ColumnTransformer(
    transformers = [
        ('StandardScale', scale, [0,1,2,3,4,5,6,7,8]),
        ('OneHotEncode', ohe, [9,10])
    ],
    remainder = 'passthrough'
)
X_train_dummy = preprocesser.fit_transform(X_train)
X_test_dummy  = preprocesser.fit_transform(X_test)
preprocesser.get_feature_names_out(col[:-1])
from sklearn.linear_model import LinearRegression,Lasso, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score
from sklearn.metrics import mean_squared_error
lr = LinearRegression()
lr.fit(X_train_dummy,y_train)
y_train.reset_index(drop=True,inplace=True)
y_test.reset_index(drop=True,inplace=True)

y_pred_lr = lr.predict(X_test_dummy)
print("Accuray Score at training data : ",lr.score(X_train_dummy, y_train))
print("Accuracy score at testing data : ",lr.score(X_test_dummy, y_test))
print("R2 Score : ",r2_score(y_test, y_pred_lr))
mse = mean_squared_error(y_test, y_pred_lr)
print("Mean Squared Error : ",mse)
rmse = np.sqrt(mse)
print("Root Mean Squared Error is : ",rmse)
mae = mean_absolute_error(y_test, y_pred_lr)
print("Mean Absolute Error : ",mae)
la = Lasso()
la.fit(X_train_dummy,y_train)
y_pred_la = la.predict(X_test_dummy)
print("Accuray Score at training data : ",la.score(X_train_dummy, y_train))
print("Accuracy score at testing data : ",la.score(X_test_dummy, y_test))
print("R2 Score : ",r2_score(y_test, y_pred_la))
mse = mean_squared_error(y_test, y_pred_la)
print("Mean Squared Error : ",mse)
rmse = np.sqrt(mse)
print("Root Mean Squared Error is : ",rmse)
mae = mean_absolute_error(y_test, y_pred_la)
print("Mean Absolute Error : ",mae)
rig = Ridge()
rig.fit(X_train_dummy, y_train)
y_pred_rig = rig.predict(X_test_dummy)
print("Accuray Score at training data : ",rig.score(X_train_dummy, y_train))
print("Accuracy score at testing data : ",rig.score(X_test_dummy, y_test))
print("R2 Score : ",r2_score(y_test, y_pred_rig))
print("Adjusted R2 : ",1-(1-r2_score(y_test, y_pred_rig))*((X_test_dummy.shape[0]-1)/(X_test_dummy.shape[0]-X_test_dummy.shape[1]-1)))
mse = mean_squared_error(y_test, y_pred_rig)
print("Mean Squared Error : ",mse)
rmse = np.sqrt(mse)
print("Root Mean Squared Error is : ",rmse)
mae = mean_absolute_error(y_test, y_pred_rig)
print("Mean Absolute Error : ",mae)
dtr = DecisionTreeRegressor(random_state=0)
dtr.fit(X_train_dummy,y_train)
y_pred_dt = dtr.predict(X_test_dummy)

print("Accuray Score at training data : ",dtr.score(X_train_dummy, y_train))
print("Accuracy score at testing data : ",dtr.score(X_test_dummy, y_test))
print("R2 Score : ",r2_score(y_test, y_pred_dt))
print("Adjusted R2 : ",1-(1-r2_score(y_test, y_pred_dt))*((X_test_dummy.shape[0]-1)/(X_test_dummy.shape[0]-X_test_dummy.shape[1]-1)))
mse = mean_squared_error(y_test, y_pred_dt)
print("Mean Squared Error : ",mse)
rmse = np.sqrt(mse)
print("Root Mean Squared Error is : ",rmse)
mae = mean_absolute_error(y_test, y_pred_dt)
print("Mean Absolute Error : ",mae)
def prediction(Year, average_rain_fall_mm_per_year,pesticides_tonnes, avg_temp, solar_radiation, soil_organic_matter, soil_nitrogen, soil_phosphorus, soil_potassium, Area, Item):
    features = np.array([[Year, average_rain_fall_mm_per_year,pesticides_tonnes, avg_temp, solar_radiation, soil_organic_matter, soil_nitrogen, soil_phosphorus, soil_potassium, Area, Item]], dtype = object)
    transform_features = preprocesser.transform(features)
    predicted_yeild = dtr.predict(transform_features).reshape(-1,1)
    return predicted_yeild[0][0]
result = prediction(1990,1485.0,121.0,16.37,16.8690215450157,4.26070373606214, 0.2722382654168,
0.0104913847700532, 1.20518328798317, 'Albania', 'Maize')
print(result)
import pickle
pickle.dump(dtr, open("dtr.pkl","wb"))
pickle.dump(preprocesser, open("preprocesser.pkl","wb"))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, mean_squared_error
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Load the data
df = pd.read_csv("expanded_yield_df.csv")

# Preprocess the data


# Encode categorical variables
ordinal_encoder = OrdinalEncoder()
df['Area'] = ordinal_encoder.fit_transform(df['Area'].values.reshape(-1, 1))
df['Item'] = ordinal_encoder.fit_transform(df['Item'].values.reshape(-1, 1))

# Split the data into training and testing sets
X = df.drop('hg/ha_yield', axis=1)
y = df['hg/ha_yield']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, shuffle=True)

# Define the VAE model
latent_dim = 2
input_dim = X_train.shape[1]

vae = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(input_dim,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(latent_dim, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(input_dim, activation='sigmoid')
])

encoder = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(input_dim,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(latent_dim, activation='relu')
])

decoder = keras.Sequential([
    layers.Dense(32, activation='relu', input_shape=(latent_dim,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(input_dim, activation='sigmoid')
])

# Compile the VAE model
vae.compile(optimizer='adam', loss='mean_squared_error')

# Train the VAE model
vae.fit(X_train.values, X_train.values, epochs=30, batch_size=32, validation_data=(X_test.values, X_test.values))

# Define the VAE-based regression model
vae_regression = keras.Sequential([
    encoder,
    layers.Dense(1)
])

vae_regression.compile(optimizer='adam', loss='mean_squared_error')

# Train the VAE-based regression model
vae_regression.fit(X_train.values, y_train.values, epochs=30, batch_size=32, validation_data=(X_test.values, y_test.values))

# Evaluate the VAE-based regression model
y_pred_vae = vae_regression.predict(X_test.values)
print("R2 Score : ", r2_score(y_test.values, y_pred_vae))
print("Mean Squared Error : ", mean_squared_error(y_test.values, y_pred_vae))
print("Root Mean Squared Error is : ", np.sqrt(mean_squared_error(y_test.values, y_pred_vae)))
print("Mean Absolute Error : ", mean_absolute_error(y_test.values, y_pred_vae))

# Define a function to make predictions using the VAE-based regression model
def prediction_vae(Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item, solar_radiation, soil_organic_matter, soil_nitrogen, soil_phosphorus, soil_potassium):
    features = np.array([[Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item, solar_radiation, soil_organic_matter, soil_nitrogen, soil_phosphorus, soil_potassium]], dtype=np.float32)
    predicted_yield = vae_regression.predict(features).reshape(-1, 1)
    return predicted_yield[0][0]

result_vae = prediction_vae(1990, 1485.0, 121.0, 16.37, 0, 0, 16.869022,	4.260704,	0.272238,	0.010491,	1.205183)  # Note: Area and Item should be encoded as integers
print("Predicted yield using VAE-based regression model : ", result_vae)

# Save the VAE-based regression model
vae_regression
