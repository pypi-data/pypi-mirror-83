#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)
import boto3
import binascii


def compare_faces(source_b64, target_b64):
    client = boto3.client('rekognition')  
    source_bytes = binascii.a2b_base64(source_b64)
    target_bytes = binascii.a2b_base64(target_b64)
    response = client.compare_faces(SimilarityThreshold=80,
                                  SourceImage={'Bytes': source_bytes},
                                  TargetImage={'Bytes': target_bytes})
    
    similarity = 0.
    for faceMatch in response['FaceMatches']:
        similarity = float(faceMatch['Similarity'])
        print('The face at ' +
               ' matches with ' + str(similarity) + '% confidence')
    
    return len(response['FaceMatches']), similarity 