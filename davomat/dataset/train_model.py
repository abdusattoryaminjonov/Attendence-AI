# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle

# load the face embeddings
print("[INFO] loading face embeddings...")
data = pickle.loads(open(r'C:/Users/asus/OneDrive/Desktop/pbl4/davomat/dataset/output/embeddings.pickle', "rb").read())
# encode the labels
print("[INFO] encoding labels...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])

# train the model used to accept the 128-d embeddings of the face and
# then produce the actual face recognition
print("[INFO] training model...")
recognizer = SVC(C=2.0, kernel="linear", tol=0.0001, decision_function_shape='ovo', probability=True)
recognizer.fit(data["embeddings"], labels)

# write the actual face recognition model to disk
f = open(r'C:/Users/asus/OneDrive/Desktop/pbl4/davomat/dataset/output/recognizer.pickle', "wb")
f.write(pickle.dumps(recognizer))
f.close()
# write the label encoder to disk
f = open(r'C:/Users/asus/OneDrive/Desktop/pbl4/davomat/dataset/output/le.pickle', "wb")
f.write(pickle.dumps(le))
f.close()
