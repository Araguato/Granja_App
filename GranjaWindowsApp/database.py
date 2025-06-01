import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from datetime import datetime

# Initialize SQLAlchemy
Base = declarative_base()
metadata = MetaData(schema='public')

class Database:
    def __init__(self):
        """Initialize the database connection"""
        # Load database configuration from environment variables
        from dotenv import load_dotenv
        import os
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Get database configuration from environment variables
        self.db_config = {
            'dbname': os.getenv('DB_NAME', 'DB_Avicola'),
            'user': os.getenv('DB_USER', 'usuario_avicola'),
            'password': os.getenv('DB_PASSWORD', 'Aves2025'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        # Create connection string
        conn_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['dbname']}"
        
        # Create engine with connection pooling
        self.engine = create_engine(
            conn_string,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800  # Recycle connections after 30 minutes
        )
        
        # Create session factory
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        
        # Reflect existing database tables
        self.reflect_tables()
    
    def reflect_tables(self):
        """Reflect database tables from existing schema"""
        # Reflect all tables from the database
        Base.metadata.reflect(bind=self.engine)
        
        # Dynamically create model classes for all tables
        for table_name in Base.metadata.tables:
            if table_name not in globals():
                # Create a new model class for the table
                cls = type(
                    table_name.capitalize(),
                    (Base,),
                    {
                        '__tablename__': table_name,
                        '__table_args__': {'extend_existing': True, 'autoload': True, 'autoload_with': self.engine},
                        '__module__': __name__
                    }
                )
                # Add the class to the global namespace
                globals()[table_name] = cls
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def close(self):
        """Close all connections in the connection pool"""
        self.Session.remove()
        self.engine.dispose()

# Define database models (these will be overridden by reflection)
# These are kept for reference and type hinting
class BaseModel(Base):
    """Base model with common fields and methods"""
    __abstract__ = True
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def get_columns(cls):
        """Get all column names for this model"""
        return [column.name for column in cls.__table__.columns]

# The actual model classes will be created dynamically during reflection

# Add more models as needed for your application
# For example: ProduccionDiaria, Mortalidad, Alimento, Venta, etc.

# Initialize the database when this module is imported
db = Database()
