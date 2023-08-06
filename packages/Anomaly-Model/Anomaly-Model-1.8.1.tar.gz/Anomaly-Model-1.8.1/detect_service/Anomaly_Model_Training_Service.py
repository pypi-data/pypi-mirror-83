# -*- coding: utf-8 -*-
"""
Created on Sept 1 20:11:03 2020

@author: Wilson
"""
import json
import numpy as np
import pandas as pd
from datetime import datetime
import time
import copy
import matplotlib.pyplot as plt
import ibm_boto3
from botocore.client import Config
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL

icos_client = ibm_boto3.client(service_name='s3',
    ibm_api_key_id='rYQmTc0U-gvfzOxV69jbUED3Fcy5QkuOL942TNeAWpT0',
    ibm_auth_endpoint="https://iam.ng.bluemix.net/oidc/token",
    config=Config(signature_version='oauth'),
    endpoint_url='https://s3.us-east.cloud-object-storage.appdomain.cloud')

bucketName='magna-formet-bucket'
bucketName_model='magna-mig-models-data'


#-----------------------------
def Read_Problem_data(model_id,icos_client,bucketName,feature_data_original,feature_data_normal):
    deviceId = model_id.split('_weld')[0] # Formet_FR4_STA60_LH_R1_weld32_toolB
    weldId_with_toolID =  model_id.split('_weld')[1]
    weld_id = int(weldId_with_toolID.split('_')[0])

    # Read Problem dta
    DR_file_name = 'Production_Anomaly_data/Formet_FR4_STA60_MIG_Weld_DR_Defects.csv'
    print(DR_file_name)
    body = icos_client.get_object(Bucket=bucketName,Key=DR_file_name)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    DR_file_df = pd.read_csv(body)
    DR_file_df = DR_file_df.drop_duplicates(subset =['PSN','WeldID'],keep='first',inplace=False)

    DR_PSN_red_list   = DR_file_df['PSN'].loc[(DR_file_df.WeldID == weld_id) & (DR_file_df.deviceId == deviceId) & (DR_file_df.Level == 'red')].tolist()
    DR_PSN_green_list = DR_file_df['PSN'].loc[(DR_file_df.WeldID == weld_id) & (DR_file_df.deviceId == deviceId) & (DR_file_df.Level == 'green')].tolist()
    DR_PSN_yellow_list = DR_file_df['PSN'].loc[(DR_file_df.WeldID == weld_id) & (DR_file_df.deviceId == deviceId) & (DR_file_df.Level == 'yellow')].tolist()
    DR_PSN_red_list = list(set(DR_PSN_red_list))
    DR_PSN_red_list.sort()
    DR_PSN_green_list = list(set(DR_PSN_green_list))
    DR_PSN_green_list.sort()
    DR_PSN_yellow_list = list(set(DR_PSN_yellow_list))
    DR_PSN_yellow_list.sort()
    
    #get RED validation data 
    validate_df = feature_data_original.loc[lambda x: (x.LPSN.isin(DR_PSN_red_list)) & (x.weld_id == weld_id),:]   
    validate_df['label'] = 1
    Data_PSN_for_red_list = validate_df['LPSN'].tolist()
    Data_PSN_for_red_list = list(set(Data_PSN_for_red_list))
    Data_PSN_for_red_list.sort()
    Data_WRI_for_red_list = validate_df['weld_record_index'].apply(lambda y: int(y)).tolist()
    Data_WRI_for_red_list = list(set(Data_WRI_for_red_list))
    Data_WRI_for_red_list.sort()
    
    # Green      
    validate_green_df = feature_data_original.loc[lambda x: (x.LPSN.isin(DR_PSN_green_list)) & (x.weld_id == weld_id),:]   
    validate_green_df['label'] = 0
    Data_PSN_for_green_list = validate_green_df['LPSN'].tolist()
    Data_PSN_for_green_list = list(set(Data_PSN_for_green_list))
    Data_PSN_for_green_list.sort()
    Data_WRI_for_green_list = validate_green_df['weld_record_index'].apply(lambda y: int(y)).tolist()
    Data_WRI_for_green_list = list(set(Data_WRI_for_green_list))
    Data_WRI_for_green_list.sort()

    # Yellow
    validate_yellow_df = feature_data_original.loc[lambda x: (x.LPSN.isin(DR_PSN_yellow_list)) & (x.weld_id == weld_id),:]   
    validate_yellow_df['label'] = 0  # .loc[row_indexer,col_indexer] 
    Data_PSN_for_yellow_list = validate_yellow_df['LPSN'].tolist()
    Data_PSN_for_yellow_list = list(set(Data_PSN_for_yellow_list))
    Data_PSN_for_yellow_list.sort()
    Data_WRI_for_yellow_list = validate_yellow_df['weld_record_index'].apply(lambda y: int(y)).tolist()
    Data_WRI_for_yellow_list = list(set(Data_WRI_for_yellow_list))
    Data_WRI_for_yellow_list.sort()

    # Cancat validation df
    validate_green_df = pd.concat([validate_green_df, validate_yellow_df])    
    validate_df = pd.concat([validate_df, validate_green_df])
    validate_df = validate_df.drop_duplicates(subset ="weld_record_index",keep='first',inplace=False)

    Data_PSN_for_all_list = validate_df['LPSN'].tolist()
    Data_PSN_for_all_list = list(set(Data_PSN_for_all_list))
    Data_PSN_for_all_list.sort()
        
    Data_WRI_for_all_list = validate_df['weld_record_index'].apply(lambda y: int(y)).tolist()
    Data_WRI_for_all_list = list(set(Data_WRI_for_all_list))
    Data_WRI_for_all_list.sort()

    PSN_WRI_dict = {}
    for i in range(len(Data_PSN_for_all_list)):
        PSN_WRI_dict[Data_WRI_for_all_list[i]] = Data_PSN_for_all_list[i]
    #print(PSN_WRI_dict)
    print('Data_PSN_for_all_list:',len(Data_PSN_for_all_list))
    print('All WRI point (weld_record_index) list = ',len(Data_WRI_for_all_list))
    print('Red WRI point list = ',len(Data_WRI_for_red_list))
    print('Green WRI point list = ',len(Data_WRI_for_green_list))
    print('Yellow WRI point list = ',len(Data_WRI_for_yellow_list))
    validation_report_df= DR_file_df.loc[lambda x: (x.PSN.isin(Data_PSN_for_all_list)) & (x.WeldID == weld_id),:]
    display(validation_report_df[['Date','PSN','FailureType','Level','WeldID','ToolID']])
    #
    # remove the defect that belongs to normal data
    #
    # get defect from normal data
    #get validation data 
    validate_normal_df = feature_data_normal.loc[lambda x: (x.LPSN.isin(DR_PSN_red_list)) & (x.weld_id == weld_id),:]

    Data_PSN_for_normal_list = validate_normal_df['LPSN'].tolist()
    Data_WRI_for_normal_list = validate_normal_df['weld_record_index'].apply(lambda y: int(y)).tolist()

    Data_PSN_removeNormal_list = list(set(Data_PSN_for_all_list) - set(Data_PSN_for_normal_list))
    Data_WRI_removeNormal_list = list(set(Data_WRI_for_all_list) - set(Data_WRI_for_normal_list))
    print('Data_PSN_removeNormal_list=',len(Data_PSN_removeNormal_list))
    print('Data_WRI_removeNormal_list=',len(Data_WRI_removeNormal_list))

    validation_wo_normal_df = validate_df.loc[lambda x: (x.LPSN.isin(Data_PSN_removeNormal_list)),:]
    #print(validation_wo_normal_df)
    
    Problem_object = {
                    'DR_file_df':DR_file_df,
                    'DR_PSN_red_list':DR_PSN_red_list,
                    'DR_PSN_green_list':DR_PSN_green_list,
                    'DR_PSN_yellow_list':DR_PSN_yellow_list,
                    'PSN_WRI_dict':PSN_WRI_dict,
                    'Data_WRI_for_red_list':Data_WRI_for_red_list,
                    'Data_WRI_for_green_list':Data_WRI_for_green_list,
                    'Data_WRI_for_yellow_list':Data_WRI_for_yellow_list,
                    'Data_PSN_for_red_list':Data_PSN_for_red_list,
                    'Data_PSN_for_green_list':Data_PSN_for_green_list,
                    'Data_PSN_for_yellow_list':Data_PSN_for_yellow_list,
                    'Data_WRI_for_all_list':Data_WRI_for_all_list,
                    'Data_PSN_for_all_list':Data_PSN_for_all_list,
                    'validate_df':validate_df,
                    'validation_wo_normal_df':validation_wo_normal_df,
                    'validation_report_df':validation_report_df
                   }
    return Problem_object


def read_feature_data(model_id,feature_file_base_list,icos_client,bucketName,COS_feature_folder,COS_feature_normal_folder,read_normal_data='Y'):
    #
    # read all feature data set from the file list
    #
    feature_data_original = pd.DataFrame()
    feature_data_normal = pd.DataFrame()

    deviceId = model_id.split('_weld')[0] # Formet_FR4_STA60_LH_R1_weld32_toolB
    toolID =  'tool'+model_id.split('_tool')[1]
    
    for feature_file_base in feature_file_base_list:
        # Read feature data
        try:
            feature_file_name = feature_file_base.replace('toolX',toolID)
            inputFile_date = feature_file_base.split('_LincolnFANUC_')[1].split('_welding_')[0]
            print(feature_file_name)
            body = icos_client.get_object(Bucket=bucketName,Key=feature_file_name)['Body']
            # add missing __iter__ method, so pandas accepts body as file-like object
            if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
            feature_data = pd.read_csv(body)
            feature_data_original = pd.concat([feature_data_original, feature_data])
        except Exception as e:
            # Just print(e) is cleaner and more likely what you want,
            # but if you insist on printing message specifically whenever possible...
            print('###### Exception, feature_data file might not exist in COS:' + feature_file_name)
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
                
        # Read normal data
        if (read_normal_data == 'Y'):
            try:
                normal_file_name = feature_file_name[:-4] + '_normal.csv'
                normal_file_name = normal_file_name.replace(COS_feature_folder,COS_feature_normal_folder)
                print(normal_file_name)
                body = icos_client.get_object(Bucket=bucketName,Key=normal_file_name)['Body']
                # add missing __iter__ method, so pandas accepts body as file-like object
                if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
                normal_data = pd.read_csv(body)
                feature_data_normal = pd.concat([feature_data_normal, normal_data])
            except Exception as e:
                # Just print(e) is cleaner and more likely what you want,
                # but if you insist on printing message specifically whenever possible...
                print('###### Exception, feature_data file might not exist in COS:' + normal_file_name)
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                

    feature_data_original = feature_data_original.reset_index(drop = True)
    if (read_normal_data == 'Y'):
        feature_data_normal = feature_data_normal.reset_index(drop = True)
        print('feature_data_normal=',feature_data_normal.shape)

    print('feature_data_original=',feature_data_original.shape)

    return feature_data_original,feature_data_normal

def read_feature_normal_data(model_id,feature_normal_file_list,icos_client,bucketName):
    #
    # read all feature data set from the file list
    #
    feature_data_normal = pd.DataFrame()

    deviceId = model_id.split('_weld')[0] # Formet_FR4_STA60_LH_R1_weld32_toolB
    toolID =  'tool'+model_id.split('_tool')[1]
    
    for feature_file_base in feature_normal_file_list:
        # Read feature data
        try:
            normal_file_name = feature_file_base.replace('toolX',toolID)
            print(normal_file_name)
            body = icos_client.get_object(Bucket=bucketName,Key=normal_file_name)['Body']
            # add missing __iter__ method, so pandas accepts body as file-like object
            if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
            normal_data = pd.read_csv(body)
            feature_data_normal = pd.concat([feature_data_normal, normal_data])
        except Exception as e:
            # Just print(e) is cleaner and more likely what you want,
            # but if you insist on printing message specifically whenever possible...
            print('###### Exception, feature_data file might not exist in COS:' + normal_file_name)
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
                                
    feature_data_normal   = feature_data_normal.reset_index(drop = True)
    print('feature_data_normal=',feature_data_normal.shape)
    return feature_data_normal

#--------------------------------------------------------------------
def export_training_validation_to_COS(model_id,icos_client,bucketName_model,feature_data_original,feature_data_normal,validate_df,validation_wo_normal_df,dateRange='',localPath='./Production_Anomaly_data/'):
    # Note: using model_id for file name in COS
    # Train
    fileName = 'Train_'+model_id+dateRange+'.csv'
            
    localfileName=localPath+fileName
    feature_data_normal.to_csv(localfileName,index=False)
    # write to COS 
    csv_fileName=model_id+'/'+ fileName
    icos_client.upload_file(Filename=localfileName,Bucket=bucketName_model,Key=csv_fileName)
    print('write to COS:'+csv_fileName)

    # original feature data
    fileName = 'Original_feature_data_'+model_id+dateRange+'.csv'
    localfileName=localPath+fileName
    feature_data_original.to_csv(localfileName,index=False)
    # write to COS 
    csv_fileName=model_id+'/'+ fileName
    icos_client.upload_file(Filename=localfileName,Bucket=bucketName_model,Key=csv_fileName)
    print('write to COS:'+csv_fileName)

    # validation
    fileName = 'validation_'+model_id+dateRange+'.csv'
    localfileName=localPath+fileName
    validate_df.to_csv(localfileName,index=False)
    # write to COS 
    csv_fileName=model_id+'/'+ fileName
    icos_client.upload_file(Filename=localfileName,Bucket=bucketName_model,Key=csv_fileName)
    print('write to COS:'+csv_fileName)

    # validation_without_normal
    fileName = 'validation_wo_normal_'+model_id+dateRange+'.csv'
    localfileName=localPath+fileName
    validation_wo_normal_df.to_csv(localfileName,index=False)
    # write to COS 
    csv_fileName=model_id+'/'+ fileName
    icos_client.upload_file(Filename=localfileName,Bucket=bucketName_model,Key=csv_fileName)
    print('write to COS:'+csv_fileName)
    return

def read_training_validation_from_COS(model_id,icos_client,bucketName,bucketName_model,testData_date_list,COS_folder_source,dateRange='',join_validation_data=False):    #
    #############################################################################################    
    # Training data
    #COS_folder_source= 'Production_Lincoln_features_data/' # original
    #COS_folder_source=  'Production_Lincoln_TSA_features_data/' # TSA
    #-----------------------------------------------------------------------------------------
    csv_fileName=model_id+'/Train_'+model_id+dateRange+'.csv'
    body = icos_client.get_object(Bucket=bucketName_model,Key=csv_fileName)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    feature_data_normal = pd.read_csv(body)
    print('feature_data_normal = ',feature_data_normal.shape)
    
    # Raw data
    csv_fileName=model_id+'/Original_feature_data_'+model_id+dateRange+'.csv'
    body = icos_client.get_object(Bucket=bucketName_model,Key=csv_fileName)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    feature_data_original = pd.read_csv(body)
    print('feature_data_original = ',feature_data_original.shape)   
    
    #############################################################################################    
    # validation data
    csv_fileName=model_id+'/validation_'+model_id+dateRange+'.csv'
    body = icos_client.get_object(Bucket=bucketName_model,Key=csv_fileName)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    validate_df = pd.read_csv(body)
    print ('Validation Data=',validate_df.shape)
    #############################################################################################
    # validation_wo_normal data
    csv_fileName=model_id+'/validation_wo_normal_'+model_id+dateRange+'.csv'
    body = icos_client.get_object(Bucket=bucketName_model,Key=csv_fileName)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    validation_wo_normal_df = pd.read_csv(body)
    print ('Validation_without_normal Data=',validation_wo_normal_df.shape)

    ##############################################################################################
    #
    # === testDate date
    #
    #testData_date_list = ['2020-08-24','2020-08-25']
    # 
    deviceId = model_id.split('_weld')[0] # Formet_FR4_STA60_LH_R1_weld32_toolB
    weldId_with_toolID =  model_id.split('_weld')[1]
    # get test data
    testData_join = pd.DataFrame()
    for weldDay in testData_date_list:
        try:
            feature_file_name = COS_folder_source+deviceId+'_LincolnFANUC_'+weldDay+'_welding_stable_data_weldid_'+weldId_with_toolID+'_feature.csv'
            body = icos_client.get_object(Bucket=bucketName,Key=feature_file_name)['Body']
            # add missing __iter__ method, so pandas accepts body as file-like object
            if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
            testData1 = pd.read_csv(body)
            testData_join = pd.concat([testData_join, testData1])
            print('add testData:',feature_file_name)
        except Exception as e:
            # Just print(e) is cleaner and more likely what you want,
            # but if you insist on printing message specifically whenever possible...
            print('###### Exception in read_training_validation_from_COS, COS name=',feature_file_name)
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
        
#     if ('current_rms_min_resi' in  testData_join.columns):
#         pass
#     else:
#         testData_join   = add_TSA_trend_and_residual(testData_join)

    if (join_validation_data == True):
        validate_noLabel_df = validate_df[testData_join.columns]
        #testData_join = pd.concat([testData_join,validate_df.loc[validate_df.label == 1]], sort=True).reset_index(drop=True)
        testData_join = pd.concat([testData_join,validate_noLabel_df], sort=True).reset_index(drop=True)
        
    testData_join = testData_join.drop_duplicates(subset ="weld_record_index",keep='first',inplace=False)

    testData = testData_join.sort_values(['weld_record_index'],inplace=False).reset_index(drop=True)   
    print ('test Data=',testData.shape)
    
    return feature_data_original,feature_data_normal,validate_df,validation_wo_normal_df,testData
#----------------------------------------------------------------
#
# add anomaly score as one column of feature csv file, and save it to COS
#----------------------------------------------------------------
def print_and_plot_anomaly_score(model_id,model_name,df_join_TF,Problem_object,anomaly_threshold,anomaly_score,percentile_point_95,plot_anomaly_score='YES'):
    deviceId = model_id.split('_weld')[0] # Formet_FR4_STA60_LH_R1_weld32_toolB
    weldId_with_toolID =  model_id.split('_weld')[1]
    weld_id = int(weldId_with_toolID.split('_')[0])

    # get from problem report:
    DR_file_df = Problem_object['DR_file_df']
    DR_PSN_red_list = Problem_object['DR_PSN_red_list']
    DR_PSN_green_list = Problem_object['DR_PSN_green_list']
    PSN_WRI_dict = Problem_object['PSN_WRI_dict']
    Data_WRI_for_red_list = Problem_object['Data_WRI_for_red_list']
    Data_WRI_for_green_list = Problem_object['Data_WRI_for_green_list']
    Data_WRI_for_yellow_list = Problem_object['Data_WRI_for_yellow_list']
    Data_WRI_for_all_list = Problem_object['Data_WRI_for_all_list']
   
    print('percentile_point_95 : ',percentile_point_95)
    outlier95_list = list(set(df_join_TF.loc[lambda x: (x.anomaly_score >= percentile_point_95), 'weld_record_index']))
    anomaly_above_threshold_list = list(set(df_join_TF.loc[lambda x: (x.anomaly_score >= anomaly_threshold), 'weld_record_index']))
    #print('outlier95_list: ', outlier90_list)
    num_red_points_above_95 = len( set(outlier95_list) & set(Data_WRI_for_red_list) )
    num_anomaly_above_95 = len(outlier95_list)
    anomaly_above_threshold_join_defects =  list(set(anomaly_above_threshold_list) & set(Data_WRI_for_red_list))
    # normal
    normal_below_threshold_list = list(set(df_join_TF.loc[lambda x: (x.anomaly_score < anomaly_threshold), 'weld_record_index']))
    normal_green_list = list(set(normal_below_threshold_list) & set(Data_WRI_for_green_list))
    num_normal_below_threshold = len(normal_below_threshold_list)
    num_normal_green_list = len(normal_green_list)
    
    
    # plot anomaly score
    if (plot_anomaly_score == 'YES'):
        plt.figure(figsize=(20,4))
        Y = anomaly_score.loc[: , 0]
        X = list(range(len(Y)))
        plt.scatter(X, Y) 
        #plt.plot(anomaly_score)
        plt.title('Anomaly Score of each Weld based on Model ' + model_name)
        plt.xlabel('Observation')
        plt.ylabel('Anomaly Score')
        plt.axhline(y=percentile_point_95, ls="--", c="red")
        plt.axhline(y=anomaly_threshold, ls="--", c="yellow")
        # bad welds:
        plot_problem_data(Data_WRI_for_red_list, df_join_TF, 'anomaly_score', "red")
        # normal welds"
        plot_problem_data(Data_WRI_for_green_list, df_join_TF , 'anomaly_score', "green")
        plot_problem_data(Data_WRI_for_yellow_list, df_join_TF , 'anomaly_score', "orange")        
        plt.show()
        
    if (plot_anomaly_score == 'YES'):
        period = 29 
        stl_res = STL(anomaly_score[0],period=period,robust=True).fit()
        plt.figure(figsize=(20,4))
        plt.plot(stl_res.trend)
        plt.title('Anomaly Score Trend based on Model ' + model_name)
        plt.xlabel('Time Steps')
        plt.ylabel('Anomaly Trend')
    
        plt.axhline(y=percentile_point_95, ls="--", c="red")
        plt.axhline(y=anomaly_threshold, ls="--", c="yellow")
        # bad welds:
        plot_problem_data(Data_WRI_for_red_list, df_join_TF, 'anomaly_score', "red")
        # normal welds"
        plot_problem_data(Data_WRI_for_green_list, df_join_TF , 'anomaly_score', "green")
        plot_problem_data(Data_WRI_for_yellow_list, df_join_TF , 'anomaly_score', "orange")
        plt.show()
    
    
    # print
    df_join_PSN_TF = df_join_TF.rename(columns={"LPSN": "PSN"})
    # abnormal points
    num_total_test = len(anomaly_score)
    num_anomaly_list_PSN = [PSN_WRI_dict[x] for x in anomaly_above_threshold_join_defects]
    num_anomaly_df = DR_file_df.loc[lambda x: (x.PSN.isin(num_anomaly_list_PSN)) & (x.WeldID == weld_id),:]

    num_anomaly_df = num_anomaly_df.merge(df_join_PSN_TF[['PSN','anomaly_score']],on = ['PSN'], how = 'left')
    num_anomaly_df = num_anomaly_df.drop_duplicates(subset ="PSN",keep='first',inplace=False)
    num_anomaly_threshold = num_anomaly_df.shape[0]

    # normal points
    num_green_list_PSN = [PSN_WRI_dict[x] for x in normal_green_list]
    num_green_df = DR_file_df.loc[lambda x: (x.PSN.isin(num_green_list_PSN)) & (x.WeldID == weld_id),:]
    
    num_total_validation = len(Data_WRI_for_all_list)
    num_total_red = len(Data_WRI_for_red_list)
    num_total_green = len(Data_WRI_for_green_list)
    num_total_yellow = len(Data_WRI_for_yellow_list)
    
    num_green_df = num_green_df.merge(df_join_PSN_TF[['PSN','anomaly_score']],on = ['PSN'], how = 'left')
    num_green_df = num_green_df.drop_duplicates(subset ="PSN",keep='first',inplace=False)
    
    print('=========number of anomaly =============== \n total test #=',num_total_test,', total validation #=', num_total_validation,', total red=',num_total_red,', total green=',num_total_green,', total yellow= ',num_total_yellow)
    print('# red above percentile_95:',num_red_points_above_95,', bad num above threshold:',num_anomaly_threshold, ', # welds above percentile_95:',num_anomaly_above_95)
    print('---------number of normal ---------------- \n green below threshold:',num_normal_green_list,', total num welds below threshold:',num_normal_below_threshold)
    display(num_anomaly_df[['Date','PSN','FailureType','anomaly_score','Level','ToolID']])
    print('--------------------------------\n')
    display(num_green_df[['Date','PSN','FailureType','anomaly_score','Level','ToolID']])
    return num_red_points_above_95,num_anomaly_threshold

#
#----------- anomaly score -----------------------
def get_anomaly_score(model_id,icos_client,bucketName,pipeline,selected_features,testData_date,COS_folder_source='Production_Lincoln_TSA_features_data/',localPath='./Production_Anomaly_data/'):
    COS_folder_source= 'Production_Lincoln_features_data/' # original
    #COS_folder_source=  'Production_Lincoln_TSA_features_data/' # TSA

    deviceId = model_id.split('_weld')[0] # Formet_FR4_STA60_LH_R1_weld32_toolB
    weldId_with_toolID =  model_id.split('_weld')[1]
    feature_file_name = COS_folder_source+deviceId+'_LincolnFANUC_'+testData_date+'_welding_stable_data_weldid_'+weldId_with_toolID+'_feature.csv'
    body = icos_client.get_object(Bucket=bucketName,Key=feature_file_name)['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    feature_data = pd.read_csv(body)
    
    scoring_data = feature_data[selected_features]
    
    ###########################################################################  
    anomaly_score_initial = pipeline.predict_proba(scoring_data) 
    ###########################################################################      
    #anomaly_threshold_initial = pipeline.get_best_thresholds()

    anomaly_score = pd.DataFrame(anomaly_score_initial)
    df_anomaly_score = pd.DataFrame(anomaly_score)            
    feature_data['anomaly_score'] = anomaly_score
    #
    # --- write the scoring result to csv file
    #
    fileName = model_id+'_anomaly_score_'+testData_date+'.csv'
    localfileName=localPath+fileName
    feature_data.to_csv(localfileName,index=False)
    # write to COS 
    csv_fileName='Production_Features_and_Anomaly_Score_data/'+ fileName
    icos_client.upload_file(Filename=localfileName,Bucket=bucketName,Key=csv_fileName)
    print('write to COS:'+csv_fileName)
    return feature_data

#-----------------------------------------
#------------------add TSA components
def add_TSA_trend_and_residual(feature_data,freqInput=125):
    # feature list
    features_select_TSA = ['current_rms_min','current_rms_max', 'current_rms_mean','current_rms_std','current_cd_max',
                           'voltage_rms_min','voltage_rms_max', 'voltage_rms_mean','voltage_rms_std','voltage_cd_max',
                           'motor_current_rms_min','motor_current_rms_max','motor_current_rms_mean','motor_current_rms_std',
                           'motor_current_rms_skew','wire_feed_speed_rms_std',
                           'power_rms_min','power_rms_max','power_rms_mean','power_rms_std', 'std_power','max_energy']
    
    # loop the features
    for tsa_feature in features_select_TSA:
        # original data
        res = sm.tsa.seasonal_decompose(feature_data[tsa_feature], freq=freqInput)
        df_resi = pd.DataFrame(res.resid).abs()
        df_trend = pd.DataFrame(res.trend).abs()
        feature_data[tsa_feature+'_resi'] = df_resi
        feature_data[tsa_feature+'_trend'] = df_trend
    #
    feature_data = feature_data.dropna(how = 'any', axis = 0).reset_index(drop =True)

    return feature_data
 
from datetime import datetime, timedelta
import dateutil 

def to_magna_datetime(collect_time):
    # collect_time = collect_time + timedelta(days=-13)
    time_start = collect_time + timedelta(hours=-1)
    time_end = collect_time
    datetime_str = collect_time.strftime("%Y-%m-%d")
    time_start_str = time_start.strftime("%Y-%m-%dT%H:%M")
    time_end_str = time_end.strftime("%Y-%m-%dT%H:%M")
    return datetime_str,time_start_str,time_end_str

def write_featureData_COS_scoring(model_id,feature_data,row_start,row_end,model_features,write_to_COS=1):
    po_feature_data = copy.deepcopy(feature_data[row_start:row_end])
    po_scoring_data = po_feature_data[model_features]

    welddate = po_feature_data.loc[row_end-1,'event_time']
    date_time_obj = datetime.strptime(welddate, '%Y-%m-%dT%H:%M:%S.%fZ')
    print('welddate=',welddate)

    dtobj = dateutil.parser.parse(welddate) 
    est_welddate  = dtobj.astimezone(dateutil.tz.gettz('US/Eastern'))
    print('est_welddate=',est_welddate) # 2020-09-30T00:01:15.762Z

    weld_date_now,weld_start,weld_end = to_magna_datetime(est_welddate)
    #print(weld_date_now,weld_end)

    target_folder_scoring = 'Production_Lincoln_Fanuc_feature_data/'
    target_folder_feature = 'Production_Lincoln_Fanuc_feature_data/'+weld_date_now + '/'
    print('target_folder_feature=',target_folder_feature)

    deviceId = model_id.split('_weld')[0] # Formet_FR4_STA60_LH_R1_weld32_toolB
    weldId_with_toolID =  model_id.split('_weld')[1]
    weld_id = int(weldId_with_toolID.split('_')[0])
    toolID = 'tool'+model_id.split('_tool')[1]

    target_feature_fileName = deviceId + '_welding_stable_data_weld'+str(weld_id)+'_'+toolID+'_'+weld_end+'_feature.csv'
    target_scoring_fileName = deviceId + '_welding_stable_data_weld'+str(weld_id)+'_'+toolID+'_feature.csv'
    print(target_feature_fileName,'\n',target_scoring_fileName)
    localPath='./Production_Anomaly_data/'
    local_feature_file_name = localPath + target_feature_fileName
    local_scoring_file_name = localPath + target_scoring_fileName
    print(local_feature_file_name,'\n',local_scoring_file_name)

    csv_feature_file_name = target_folder_feature + target_feature_fileName
    csv_scoring_file_name = target_folder_scoring + target_scoring_fileName
    print(csv_feature_file_name,'\n',csv_scoring_file_name)
    
    if (write_to_COS == 1):
        po_feature_data.to_csv(local_feature_file_name, index= False)
        po_scoring_data.to_csv(local_scoring_file_name, index= False)
        # to COS
        icos_client.upload_file(Filename=local_feature_file_name,Bucket=bucketName,Key=csv_feature_file_name)
        print('write to COS:'+csv_feature_file_name)
        icos_client.upload_file(Filename=local_scoring_file_name,Bucket=bucketName,Key=csv_scoring_file_name)
        print('write to COS:'+csv_scoring_file_name)

#
# ---------------------plot problem data
#
def plot_problem_data(problem_weld_list, feature_join_df , fea_name, color="red" ):
    for i in problem_weld_list:
        Y = feature_join_df.loc[feature_join_df.weld_record_index == i, fea_name ]
        X = feature_join_df.loc[feature_join_df.weld_record_index == i, : ].index.tolist()[0]
        plt.scatter(X, Y, s= 30, c = color )  # plot 点图
