from datetime import datetime

from app import db
from sqlalchemy import Column, String, Boolean, BigInteger, Integer, Text
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.models.base_model import BaseModel

class Role(BaseModel, db.Model):
    """
    Model representing a role.
    """
    __tablename__ = "roles"
    title = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    default = Column(Boolean, default=False, index=True)
    permissions = Column(BigInteger, default=0)
    isActive = Column(Boolean, default=True)

    # Back references
    users = relationship("User", back_populates="role")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return f"Role(roleId = {self.id}, title = '{self.title}')"

    @staticmethod
    def insert_roles():
        """ """
        # Assigning permissions to roles
        from app.models import Permission
        roles = {
            "Guest": [0],
            "Manufacturer": [
                Permission.GENERATE_QR_CODE, Permission.VIEW_MANUFACTURER_PRODUCTS,
                Permission.VIEW_DISTRIBUTION_DATA, Permission.UPDATE_PRODUCT
            ],
            "Wholesaler": [
                Permission.VIEW_MANUFACTURER_PRODUCTS, Permission.PLACE_ORDER,
                Permission.VIEW_DISTRIBUTION_DATA, Permission.UPDATE_ORDER_STATUS
            ],
            "Retailer": [
                Permission.VIEW_WHOLESALER_PRODUCTS, Permission.PLACE_ORDER,
                Permission.VIEW_DISTRIBUTION_DATA, Permission.VERIFY_PRODUCT
            ],
            "Farmer": [
                Permission.PLACE_ORDER, Permission.VIEW_RETAILER_PRODUCTS,
                Permission.VERIFY_PRODUCT
            ],
            "Administrator": [
                Permission.GENERATE_QR_CODE, Permission.VERIFY_PRODUCT, Permission.VIEW_ALL_PRODUCTS, Permission.VIEW_DISTRIBUTION_DATA
            ]
        }

        default_role = "Guest"
        for r in roles:
            role = Role.query.filter_by(title=r).first()
            if role is None:
                role = Role(title=r)

            role.resetPermissions()
            for perm in roles[r]:
                role.addPermission(perm)

            role.default = (role.title == default_role)
            db.session.add(role)
        db.session.commit()

    @classmethod
    def create(cls, details={}):
        """
        Create a new role.

        :param details: dict - a dictionary of role details to be saved.

        :return role: Role - the newly created Role instance.
        """
        role = Role(
            title=details.get("title"),
            description=details.get("description"),
        )

        db.session.add(role)
        db.session.commit()

        return role

    def delete(self):
        """
        Delete the role.
        """
        db.session.delete(self)
        db.session.commit()

    def updateDetails(self, details={}):
        """
        Update details of the role.

        :param details: dict - a dictionary of up to date role details.

        :return self: Role - the updated Role instance.
        """
        self.title = details.get("title")
        self.description = details.get("description")

        db.session.add(self)
        db.session.commit()

        return self

    def deactivate(self):
        """
        Deactivate a role.
        """
        if self.isActive:
            self.isActive = False

            db.session.add(self)
            db.session.commit()

        return self

    def addPermission(self, permission):
        """
        Add a permission to the role.

        :param permission: int - The permission to the added.
        """
        if not self.hasPermission(permission):
            self.permissions += permission

    def removePermission(self, permission):
        """
        Remove a permission from the role.

        :param permission: int - The permision to be removed.
        """
        if self.hasPermission(permission):
            self.permissions -= permission

    def resetPermissions(self):
        """
        Reset permissions of the role.
        """
        self.permissions = 0

    def hasPermission(self, permission):
        """
        Check if the role has a specific permission.

        :param permission: int - The permission to be checked.

        :return: bool - True if the role has the specified permission, False
            otherwise.
        """
        return self.permissions & permission == permission

    def getDetails(self):
        """
        Return role details.

        :return details: dict - a dictionary containing details of the Role
            instance.
        """
        details = {
            "roleId": self.id,
            "title": self.title,
            "description": self.description,
            "permissions": self.permissions,
            "isDefault": self.default,
            "usersCount": self.users.count(),
        }

        return details
