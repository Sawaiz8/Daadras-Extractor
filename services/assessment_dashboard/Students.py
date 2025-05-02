from sqlalchemy import Column, Integer, String, Date, Float, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from services.streamlit.main.database import Base, engine

class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    mid_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    age = Column(Integer)
    date_of_birth = Column(Date)
    gender = Column(String)
    classes_attended = Column(Integer, default=0)
    session_id = Column(Integer, ForeignKey("sessions.id"))

    session = relationship("Sessions", back_populates="students") 
    written_exam_scores = relationship("WrittenExamScores", back_populates="student")
    viva_transcripts = relationship("VivaTranscripts", back_populates="student")
    practical_exam_reports = relationship("PracticalExamReports", back_populates="student")



{
  "_id": ObjectId("..."),
  "first_name": "John",
  "mid_name": "Doe",
  "last_name": "Smith",
  "age": 20,
  "gender": "Male",
  "classes_attended": 10,
  "email": "email@example.com",
  "contact_number": "1234567890",
  "city": "City Name",
  "address": "Full Address",
  "session_id": ObjectId("session_object_id"),  
  "pre_test_data": {
    "written_exam_scores": {
      "written_ai_section_score": 85,
      "written_env_score": 90,
      "written_internet_score": 85,
      "written_canva_score": 90,
      "written_programming_score": 85,
      "written_hardware_software_score": 90,
      "other_new_section_score_aggregated": 90,
      "total_student_marks": 90,
      "total_marks_of_exam": 90,
      "start_time_exam": "2025-01-01",
      "end_time_exam": "2025-01-01"
    },
    "viva": {
      "transcript": "The kid performed well in the exam",
      "analysis": "The kid performed well in the exam"
    },
    "practical_exam_reports": {
      "report": "The kid performed well in the exam"
    },
  },
  "post_test_data": {
    "written_exam_scores": {
        "written_ai_section_score": 85,
        "written_env_score": 90,
        "written_internet_score": 85,
        "written_canva_score": 90,
        "written_programming_score": 85,
        "written_hardware_software_score": 90,
        "other_new_section_score_aggregated": 90,
        "total_student_marks": 90,
        "total_marks_of_exam": 90,
        "start_time_exam": "2025-01-01",
        "end_time_exam": "2025-01-01"
    },
    "viva": {
        "transcript": "The kid performed well in the exam",
        "analysis": "The kid performed well in the exam"
    },
    "practical_exam_reports": {
      "report": "The kid performed well in the exam"
    }
  }
}



{
    "id": 0,
    "session_id": 0,
    "session_name": "Session Name",
    "first_name": "First Name",
    "mid_name": "Middle Name",
    "last_name": "Last Name", 
    "age": 25,
    "date_of_birth": "2000-01-01",
    "gender": "Male/Female",
    "email": "email@example.com",
    "phone_number": "1234567890",
    "previous_ngo_experience": "Description of previous NGO experience",
    "city": "City Name",
    "address": "Full Address",
    "occupation": "Current Occupation",
    "institute": "Institute Name",
    "cv_link": "https://example.com/cv",
    "insta_id": "instagram_handle",
    "linked_in": "linkedin_profile_url",
    "has_discord": true,
    "classes_attended": 0,
    "forms_questions": {
        "question1": "Answer 1",
        "question2": "Answer 2",
        "question3": "Answer 3"
    }
}


{
    "session_id": 0,
    "session_name": "Session Name",
    "name": "Unique Name",
    "total_classes": 0,
    "school_name": "School Name",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
}


