"""
Simple command-line tool to upload files to CurseForge using curseuploadpy.
"""
import argparse
import logging
import os
from curseuploadpy import CurseUploadClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(
        prog='curseuploadpy',
        description='CurseForge File Uploader',
        epilog='Uploads files to CurseForge using the CurseForge Upload API')
    parser.add_argument(
        '--api-key', '-k',
        required=True,
        help='The CurseForge API key to use for authentication')
    parser.add_argument(
        '--project-id', '-p',
        required=True,
        type=int,
        help='The CurseForge project ID to upload the file to')
    parser.add_argument(
        '--file-path', '-f',
        required=True,
        help='The path to the file to upload')
    parser.add_argument(
        '--changelog-path', '-c',
        required=True,
        help='Changelog file')
    parser.add_argument(
        '--changelog-type', '-ct',
        choices=['text', 'html', 'markdown'],
        help='Changelog format. By default it is auto-detected by file extension')
    parser.add_argument(
        '--release-type', '-rt',
        required=True,
        choices=['alpha', 'beta', 'release'],
        help='The release type of the file')
    parser.add_argument(
        '--parent-file-id', '-pf',
        help='Optional parent file ID. Cannot use with game-versions')
    parser.add_argument(
        '--version', '-v',
        action='append',
        help='Append a version to associate the file with. Cannot use with parent-file-id')
    parser.add_argument(
        '--embedded-lib-dep', '-ed',
        action='append',
        help='Add an embedded library dependency slug')
    parser.add_argument(
        '--incompatible-dep', '-id',
        action='append',
        help='Add an incompatible dependency slug')
    parser.add_argument(
        '--optional-dep', '-od',
        action='append',
        help='Add an optional dependency slug')
    parser.add_argument(
        '--required-dep', '-rd',
        action='append',
        help='One or more slugs of required dependencies')
    parser.add_argument(
        '--tool-dep', '-td',
        action='append',
        help='Add a tool dependency slug')
    parser.add_argument(
        '--dryrun',
        action='store_true',
        help='Do not actually upload the file, just print the details')

    args = parser.parse_args()

    # Make sure either parent_file_id or versions is provided
    if args.parent_file_id and args.version:
        parser.error('Cannot use --parent-file-id with --versions')
    elif not args.parent_file_id and not args.version:
        parser.error('Must specify either --parent-file-id or --versions')

    # Ensure all provided files exist
    for path in [args.file_path, args.changelog_path]:
        if not os.path.exists(path):
            parser.error(f'File not found: {path}')

    # Auto-detect changelog type if not provided
    if not args.changelog_type:
        # Auto-detect changelog type
        if args.changelog_path.endswith('.html'):
            args.changelog_type = 'html'
        elif args.changelog_path.endswith('.md'):
            args.changelog_type = 'markdown'
        else:
            args.changelog_type = 'text'

    return args


def main():
    # Parse arguments
    args = parse_args()

    # Configure logging
    logger.setLevel(logging.DEBUG)

    # Read changelog
    with open(args.changelog_path, 'r') as f:
        changelog = f.read()

    # Create client
    client = CurseUploadClient(args.api_key)

    # Resolve game version IDs from given version strings
    version_ids = []
    if args.version:
        version_table = client.game_versions()
        version_ids = resolve_game_versions(version_table, args.version)

    # Handle dependencies
    deps = []
    if args.embedded_lib_dep:
        deps.extend([(dep, 'embeddedLibrary') for dep in args.embedded_lib_dep])
    if args.incompatible_dep:
        deps.extend([(dep, 'incompatible') for dep in args.incompatible_dep])
    if args.optional_dep:
        deps.extend([(dep, 'optionalDependency') for dep in args.optional_dep])
    if args.required_dep:
        deps.extend([(dep, 'requiredDependency') for dep in args.required_dep])
    if args.tool_dep:
        deps.extend([(dep, 'tool') for dep in args.tool_dep])

    logger.info("Project upload details: ")
    logger.info(f" - Project ID: {args.project_id}")
    logger.info(f" - File Path: {args.file_path}")
    logger.info(f" - Changelog Path: {args.changelog_path}")
    logger.info(f" - Changelog Type: {args.changelog_type}")
    logger.info(f" - Release Type: {args.release_type}")
    logger.info(f" - Parent File ID: {args.parent_file_id}")
    logger.info(f" - Version IDs: {version_ids}")
    logger.info(f" - Dep map: {deps}")

    logger.info("Uploading file...")
    if args.dryrun:
        logger.info("Dry run mode enabled, skipping upload")
        exit(0)

    response = client.upload_file(
        project_id=args.project_id,
        file_path=args.file_path,
        changelog=changelog,
        changelog_type=args.changelog_type,
        releaseType=args.release_type,
        parent_file_id=args.parent_file_id,
        game_versions=version_ids if len(version_ids) > 0 else None,
        deps=deps if len(deps) > 0 else None
    )

    logger.info(f"Upload response: {response}")
    exit(0)


def resolve_game_versions(curse_versions_table, version_strings):
    logger.info(f"Attempting to map versions: {version_strings}")

    version_ids = []
    for version in version_strings:
        for v in curse_versions_table:
            if v['name'] == version:
                logger.debug(f"Mapped via name: '{version}' -> {v['id']}")
                version_ids.append(v['id'])
                break
            elif v['slug'] == version:
                logger.debug(f"Mapped via slug: '{version}' -> {v['id']}")
                version_ids.append(v['id'])
        else:
            logger.error(f"Unable to map '{version}'")
            exit(1)

    logger.info(f"Mapped versions: {version_ids}")
    return version_ids


if __name__ == '__main__':
    main()
