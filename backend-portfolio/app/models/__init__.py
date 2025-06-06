from app.db.session import Base
from app.models.article import Article
from app.models.skills import Skill, SkillUser, SkillCategory
from app.models.user import User
from app.models.project import Project
# Import any other models here

# This allows Base.metadata.create_all() to discover all models