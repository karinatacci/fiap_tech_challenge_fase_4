import cv2
import mediapipe as mp
from deepface import DeepFace
from collections import Counter
from tqdm import tqdm
import numpy as np

def main():
    video_path = "video_tech_challenge.mp4"
    output_video_path = "video_tech_challenge_final_final.mp4"
    output_summary_path = "video_summary_final_final.txt"
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erro ao carregar o vídeo.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.7)
    mp_pose = mp.solutions.pose.Pose()
    
    activity_summary = []
    emotions_summary = []
    anomalies_count = 0
    frame_skip_interval = 10  # Processar 1 em cada 10 frames
    last_activity = None
    stable_activity_count = 0
    min_frames_for_stable_activity = 5  # Persistência mínima para confirmar atividade
    detected_activities = set()  # Armazenar atividades únicas já detectadas

    with tqdm(total=frame_count, desc="Processando vídeo") as pbar:
        for current_frame in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break

            if current_frame % frame_skip_interval != 0:
                pbar.update(1)
               # continue

            # Detectar rostos e emoções
            frame, detected_emotions = detect_and_mark_faces_and_emotions(frame, mp_face_detection)
            if detected_emotions:
                emotions_summary.extend(detected_emotions)

            # Detectar atividades
            activity, is_anomalous = detect_activity(frame, mp_pose)

            # Registrar apenas a primeira ocorrência de uma atividade
            if activity and activity not in detected_activities:
                detected_activities.add(activity)
                activity_summary.append(activity)
                cv2.putText(frame, f"Atividade: {activity}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

            if is_anomalous:
                anomalies_count += 1

            out.write(frame)
            pbar.update(1)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    generate_summary(activity_summary, emotions_summary, output_summary_path, frame_count, anomalies_count)
    print(f"Vídeo processado e salvo como {output_video_path}")
    print(f"Resumo salvo em {output_summary_path}")

def detect_and_mark_faces_and_emotions(frame, mp_face_detection):
    detected_emotions = []
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face_detection.process(frame_rgb)

    if results.detections:
        detections = sorted(results.detections, key=lambda d: d.location_data.relative_bounding_box.width, reverse=True)
        for detection in detections[:1]:  # Processar apenas o maior rosto
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            left, top, width, height = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
            right, bottom = left + width, top + height

            if left > w * 0.3 and right < w * 0.7:  # Apenas rostos no centro
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                face_frame = frame[top:bottom, left:right]
                try:
                    result = DeepFace.analyze(face_frame, actions=['emotion'], enforce_detection=True)
                    if result:
                        emotion = result[0]['dominant_emotion']
                        confidence = result[0]['emotion'][emotion]
                        if confidence > 0.8:  # Filtrar emoções por alta confiança
                            detected_emotions.append(emotion)
                            cv2.putText(frame, emotion, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                except Exception:
                    pass

    return frame, detected_emotions

def detect_activity(frame, mp_pose):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_pose.process(frame_rgb)

    is_anomalous = False

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        try:
            left_hand_y = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST].y
            right_hand_y = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST].y
            head_y = landmarks[mp.solutions.pose.PoseLandmark.NOSE].y
            left_shoulder_y = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].y
            right_shoulder_y = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].y

            # Refinando condições para atividades
            if abs(left_hand_y - head_y) < 0.15 and abs(right_hand_y - head_y) < 0.15:
                activity = "Pessoa lendo"
            elif left_hand_y < left_shoulder_y and right_hand_y > right_shoulder_y:
                activity = "Pessoa acenando para a câmera"
            elif left_hand_y > left_shoulder_y and right_hand_y > right_shoulder_y and abs(left_hand_y - right_hand_y) < 0.3:
                activity = "Pessoa dançando"
            elif left_hand_y < head_y or right_hand_y < head_y:
                activity = "Pessoa mexendo no celular"
            else:
                activity = "Atividade não identificada"
                is_anomalous = True

            return activity, is_anomalous
        except IndexError:
            return None, True

    return None, True

def generate_summary(activities, emotions, output_path, frame_count, anomalies_count):
    activity_counter = Counter(activities)
    emotion_counter = Counter(emotions)

    with open(output_path, "w") as f:
        f.write("Resumo do vídeo:\n\n")
        f.write(f"Total de frames analisados: {frame_count}\n")
        f.write(f"Número de anomalias detectadas: {anomalies_count}\n\n")

        f.write("Atividades detectadas:\n")
        for activity, count in activity_counter.items():
            f.write(f"- {activity}: detectado {count} vezes\n")

        f.write("\nEmoções predominantes:\n")
        for emotion, count in emotion_counter.items():
            f.write(f"- {emotion}: detectado {count} vezes\n")

        f.write("\nAnálise geral:\n")
        if activity_counter:
            most_common_activity = activity_counter.most_common(1)[0]
            f.write(f"A atividade mais frequente no vídeo foi '{most_common_activity[0]}', "
                    f"ocorrendo aproximadamente {most_common_activity[1]} vezes.\n")

        if emotion_counter:
            most_common_emotion = emotion_counter.most_common(1)[0]
            f.write(f"A emoção predominante foi '{most_common_emotion[0]}', "
                    f"aparecendo em aproximadamente {most_common_emotion[1]} quadros.\n")

    print(f"Resumo salvo em {output_path}")

if __name__ == "__main__":
    main()