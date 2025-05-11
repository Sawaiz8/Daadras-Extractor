
# if [ ! -f alembic/versions/*.py ]; then
#   # Create migration if not already generated
#   echo "Creating Alembic migration..."
#   alembic revision --autogenerate -m "Initial migration"
# fi
# alembic upgrade head
streamlit run app.py --server.address 0.0.0.0 --server.port 8501