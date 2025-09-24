from common.models.base_schema import BaseSchema


class CreateInvitationDto(BaseSchema):
    invitee_email: str
