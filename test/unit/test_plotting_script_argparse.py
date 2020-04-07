import subprocess
from unittest.mock import Mock

from ash_model_plotting import plot_ash_model_results as pamr


def test_pamr_argparse(tmpdir, script_dir, data_dir):
    # Arrange
    script_path = script_dir / 'plot_ash_model_results.py'
    input_file = data_dir / 'fall3d_operational.nc'
    model_type = 'name'
    limits = (1, 2, 3, 4)
    pamr.plot_results = Mock()

    # This test will throw error if
    # Call with no args
    subprocess.run(['python', script_path, input_file])
    subprocess.run(
        ['python', script_path, input_file, '--model_type', model_type,
         '--limits', *[str(l) for l in limits], '--output_dir', tmpdir])
