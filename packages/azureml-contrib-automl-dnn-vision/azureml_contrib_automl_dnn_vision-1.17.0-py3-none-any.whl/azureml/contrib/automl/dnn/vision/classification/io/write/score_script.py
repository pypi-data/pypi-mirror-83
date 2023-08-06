# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Score images from model produced by another run."""

from azureml.train.automl import constants
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.utils import _exception_handler, _set_logging_parameters
from azureml.contrib.automl.dnn.vision.classification.inference.score import score
import argparse

logger = get_logger(__name__)


@_exception_handler
def main():
    """Wrapper method to execute script only when called and not when imported."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_id', help='run id of the experiment that generated the model')
    parser.add_argument('--experiment_name', help='experiment that ran the run which generated the model')
    parser.add_argument('--output_file', help='path to output file')
    parser.add_argument('--root_dir', help='path to root dir for files listed in image_list_file')
    parser.add_argument('--image_list_file', help='image files list')
    parser.add_argument('--output_dataset_target_path', help='datastore target path for output dataset files')
    parser.add_argument('--input_dataset_id', help='input dataset id')

    args, unknown = parser.parse_known_args()

    # Set up logging
    task_type = constants.Tasks.IMAGE_CLASSIFICATION
    _set_logging_parameters(task_type, args)

    # TODO JEDI
    # When we expose the package to customers we need to revisit. We should not log any unknown
    # args when the customers send their hp space.
    if unknown:
        logger.info("Got unknown args, will ignore them: {}".format(unknown))

    score(args.run_id, experiment_name=args.experiment_name, output_file=args.output_file,
          root_dir=args.root_dir, image_list_file=args.image_list_file,
          output_dataset_target_path=args.output_dataset_target_path,
          input_dataset_id=args.input_dataset_id)


if __name__ == "__main__":
    # execute only if run as a script
    main()
