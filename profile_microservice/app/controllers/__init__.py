from app.controllers.profiles import ProfileModelController
from app.models.profiles import Profile as ProfileModel

profile_controller = ProfileModelController(ProfileModel)