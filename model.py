from sqlalchemy import Column, Integer, String, Date, Float, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine



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


class Volunteers(Base):
    __tablename__ = "volunteers"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    session_name = Column(String)
    first_name = Column(String, nullable=False)
    mid_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    age = Column(Integer)
    date_of_birth = Column(Date)
    gender = Column(String)
    email = Column(String)
    phone_number = Column(String)
    previous_ngo_experience = Column(String)
    city = Column(String)
    address = Column(String)
    occupation = Column(String)
    institute = Column(String)
    cv_link = Column(String)
    insta_id = Column(String)
    linked_in = Column(String)
    has_discord = Column(Boolean)
    classes_attended = Column(Integer, default=0)
    
    session = relationship("Sessions", back_populates="volunteers") 
    viva_transcripts = relationship("VivaTranscripts", back_populates="volunteer")
    practical_exam_reports = relationship("PracticalExamReports", back_populates="volunteer")


class WrittenExamScores(Base):
    __tablename__ = "written_exam_scores"
    
    id = Column(Integer, primary_key=True)
    exam_type = Column(String)
    exam_date = Column(Date)
    written_ai_section_score = Column(Float)
    written_env_score = Column(Float)
    written_internet_score = Column(Float)
    written_canva_score = Column(Float)
    written_programming_score = Column(Float)
    written_hardware_software_score = Column(Float)
    other_new_section_score_aggregated = Column(Float)
    total_student_marks = Column(Float)
    total_marks_of_exam = Column(Float)
    start_time_exam = Column(Time)
    end_time_exam = Column(Time)
    student_id = Column(Integer, ForeignKey("students.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))
    
    student = relationship("Students", back_populates="written_exam_scores")
    session = relationship("Sessions", back_populates="written_exam_scores")


class VivaTranscripts(Base):
    __tablename__ = "viva_transcripts"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"))
    exam_type = Column(String)
    exam_date = Column(Date)
    transcript = Column(String)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    
    student = relationship("Students", back_populates="viva_transcripts")
    volunteer = relationship("Volunteers", back_populates="viva_transcripts")
    session = relationship("Sessions", back_populates="viva_transcripts")


class PracticalExamReports(Base):
    __tablename__ = "practical_exam_reports"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"))
    exam_type = Column(String)
    exam_date = Column(Date)
    report = Column(String)
    
    student = relationship("Students", back_populates="practical_exam_reports")
    volunteer = relationship("Volunteers", back_populates="practical_exam_reports")
    session = relationship("Sessions", back_populates="practical_exam_reports")


class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True)
    total_classes = Column(Integer, default=0)
    school_name = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    
    students = relationship("Students", back_populates="session")
    volunteers = relationship("Volunteers", back_populates="session")
    written_exam_scores = relationship("WrittenExamScores", back_populates="session")
    viva_transcripts = relationship("VivaTranscripts", back_populates="session")
    practical_exam_reports = relationship("PracticalExamReports", back_populates="session")



Base.metadata.create_all(bind=engine)
