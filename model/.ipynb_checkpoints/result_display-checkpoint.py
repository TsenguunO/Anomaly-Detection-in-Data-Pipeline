from datetime import datetime
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay,classification_report,make_scorer, f1_score, accuracy_score
import matplotlib.pyplot as plt
import pandas as pd
#show result in confusion matrix plot and return model metric 
def show_result(test,pred):
        
    cm = confusion_matrix(test, pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.savefig("confusion_matrix.png")
    #plt.show()
    report = classification_report(test, pred, output_dict=True)    

    precision = report['weighted avg']['precision']
    recall = report['weighted avg']['recall']
    f1_score = report['weighted avg']['f1-score']
    return precision, recall, f1_score
    
def export_anomaly(original_df, pred_list):
    now = datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S")
    label_series = pd.Series(pred_list)
    anomalies= original_df[label_series == 1]
    filename = f"export_anomaly/anomaly_{date_time}.csv"
    anomalies.to_csv(filename, index=False)
    return 0