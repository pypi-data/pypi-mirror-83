import glob
import json

from beneath.client import Client
from beneath.utils import StreamQualifier
from beneath.cli.utils import async_cmd, str2bool, pretty_print_graphql_result


def add_subparser(root):
  model = root.add_parser('model').add_subparsers()

  _init = model.add_parser('init')
  _init.set_defaults(func=async_cmd(init))
  _init.add_argument('model_path', type=str)

  _delete = model.add_parser('delete')
  _delete.set_defaults(func=async_cmd(delete))
  _delete.add_argument(
    '--confirm',
    type=str2bool,
    required=True,
    nargs='?',
    const=True,
    default=False,
  )

  _stage = model.add_parser('stage')
  _stage.set_defaults(func=async_cmd(stage))
  _stage.add_argument('--update', type=str2bool, nargs='?', const=True, default=False)


async def init(args):
  raise Exception("Not implemented")


async def delete(args):
  with open("config.json", "r") as f:
    conf = json.load(f)

  client = Client()

  model = await client.admin.models.find_by_organization_project_and_name(
    organization_name=conf.get("organization", None),
    project_name=conf.get("project", None),
    model_name=conf.get("name", None),
  )

  result = await client.admin.models.delete(model["modelID"])
  pretty_print_graphql_result(result)


async def stage(args):
  # read config
  with open("config.json", "r") as f:
    conf = json.load(f)

  # read schemas
  def _read_schema(path):
    with open(path, "r") as f:
      return f.read()

  schemas = [_read_schema(p) for p in glob.glob("schemas/*.graphql")]

  # get client
  client = Client()

  # get params
  organization_name = conf.get("organization", None)
  project_name = conf.get("project", None)
  model_name = conf.get("name", None)

  # get project
  result = await client.admin.projects.find_by_organization_and_name(
    organization_name=organization_name,
    project_name=project_name,
  )
  project_id = result['projectID']
  project_name = result['name']

  # get input stream IDs
  input_stream_ids = []
  for dep in conf.get("dependencies", []):
    sq = StreamQualifier.from_path(dep)
    details = await client.admin.streams.find_by_organization_project_and_name(
      organization_name=sq.organization,
      project_name=sq.project,
      stream_name=sq.stream,
    )
    input_stream_ids.append(details["streamID"])

  # stage model
  if args.update:
    model = await client.admin.models.find_by_organization_project_and_name(
      organization_name=organization_name,
      project_name=project_name,
      model_name=model_name,
    )
    result = await client.admin.models.update(
      model_id=model["modelID"],
      source_url=conf.get("source_url", None),
      description=conf.get("description", None),
      input_stream_ids=input_stream_ids,
      output_stream_schemas=schemas,
    )
  else:
    result = await client.admin.models.create(
      name=model_name,
      project_id=project_id,
      kind=conf.get("kind", None),
      source_url=conf.get("source_url", None),
      description=conf.get("description", None),
      input_stream_ids=input_stream_ids,
      output_stream_schemas=schemas,
    )

  # print out model details
  pretty_print_graphql_result(result)
