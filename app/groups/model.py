from app.db.session import Base


class FamilyGroupMember(Base):
    __tablename__ = "family_group_memebers"
    pass


class FamilyGroup(Base):
    __tablename__ = "family_groups"
    pass
