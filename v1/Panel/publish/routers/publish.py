
from common.exceptions import NotAcceptableError
from config import env_config
from fastapi import APIRouter, Request, status

from engines.rate_limiter import limiter

from common.resources import response_data
from v1.Panel.publish.schemas import PublishPostIn
from ..dependencies import create_command, get_all_configs, run_command


from common.schemas import UniqueResponse

router = APIRouter(prefix="/publish")


@router.post("/from_script", status_code=status.HTTP_202_ACCEPTED)
# @limiter.limit('1/minutes')
async def publish_from_scrypt(
        request: Request,
        data: PublishPostIn
):

    conf = await get_all_configs(env_config.CONF_PATH)

    if data.project_name not in conf.keys():
        raise NotAcceptableError("project name not valid")

    conf = conf[data.project_name]
    arg_obj = {}
    if 'args' in conf:
        try:
            arg_obj = {key.lower(): value for key, value in (
                pair.split(':') for pair in data.args)}
        except:
            raise NotAcceptableError("args not valid")

        for c in conf['args']:
            if c not in arg_obj:
                raise NotAcceptableError(f"({c}) not in args")

    try:
        if data.backup and 'backup' in conf and len(conf['backup']):
            for c in conf['backup']:
                for a in conf['args']:
                    c = c.replace(f"#{a}", arg_obj[a])
                run_command(create_command(c), conf["work_dir"])

        if 'update' in conf and len(conf['update']):

            for c in conf['update']:
                for a in conf['args']:
                    c = c.replace(f"#{a}", arg_obj[a])
                run_command(create_command(c), conf["work_dir"])

    except Exception as e:
        raise UniqueResponse(f"ERROR : {e}")

    return UniqueResponse(response_data.ACCEPTED)
