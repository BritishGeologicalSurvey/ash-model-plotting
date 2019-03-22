from textwrap import dedent

from ash_model_plotting.plotting import render_html

EXPECTED_3D = dedent("""
<!DOCTYPE html>
<html>
  <head>
    <title>VA_Tutorial - Total deposition - 0904UTC 20/07/2018</title>
    <style type="text/css">
      h3, h4, h5 {
        color: grey;
        font-family: sans-serif;
      }

      table {
        border-collapse: collapse;
      }

      blockquote {
        font-family: "Courier New", Courier, monospace;
      }

      th, td {
        text-align: left;
        padding: 8px;
      }

      tr:nth-child(even) {
        background-color: #f2f2f2;
      }
    </style>
  </head>

  <body>

  <h3>VA_Tutorial - Total deposition - 0904UTC 20/07/2018</h3>

  <hr>
  <h4>Attributes</h4>

  <blockquote>
    <b>Source data:</b> some source<br>
    <b>End of release:</b> 0800UTC 17/04/2010<br>
    <b>Forecast duration:</b> 75 hours<br>
    <b>Met data:</b> NWP Flow.ECMWF ERAInt Regional<br>
    <b>NAME Version:</b> NAME III (version 7.2)<br>
    <b>Release height:</b> 1651.000 to 6151.000m asl<br>
    <b>Release location:</b> 19.3600W   63.3700N<br>
    <b>Release rate:</b> 9.4444448E+07g/s<br>
    <b>Run time:</b> 0904UTC 20/07/2018<br>
    <b>Species:</b> VOLCANIC_ASH<br>
    <b>Species Category:</b> VOLCANIC<br>
    <b>Start of release:</b> 0000UTC 17/04/2010<br>
    <b>Title:</b> VA_Tutorial<br>
    <b>Conventions:</b> CF-1.5<br>
    <b>Quantity:</b> Total deposition<br>
    <b>Time Av or Int:</b> 078 hr time integrated<br>
  </blockquote>

  <hr>
  <h4>Plots</h4>

    <table>
      <tr><td>
        <a href="VA_Tutorial_Total_deposition_20100418030000.png">
          <img src="VA_Tutorial_Total_deposition_20100418030000.png" width="640">
        </a>
      </td></tr>
      <tr><td>
        <a href="VA_Tutorial_Total_deposition_20100418060000.png">
          <img src="VA_Tutorial_Total_deposition_20100418060000.png" width="640">
        </a>
      </td></tr>
      </table>

  </body>
</html>
""").strip()


EXPECTED_4D = dedent("""
<!DOCTYPE html>
<html>
  <head>
    <title>VA_Tutorial - Air Concentration - 0904UTC 20/07/2018</title>
    <style type="text/css">
      h3, h4, h5 {
        color: grey;
        font-family: sans-serif;
      }

      table {
        border-collapse: collapse;
      }

      blockquote {
        font-family: "Courier New", Courier, monospace;
      }

      th, td {
        text-align: left;
        padding: 8px;
      }

      tr:nth-child(even) {
        background-color: #f2f2f2;
      }
    </style>
  </head>

  <body>

  <h3>VA_Tutorial - Air Concentration - 0904UTC 20/07/2018</h3>

  <hr>
  <h4>Attributes</h4>

  <blockquote>
    <b>Source data:</b> some source<br>
    <b>End of release:</b> 0800UTC 17/04/2010<br>
    <b>Forecast duration:</b> 75 hours<br>
    <b>Met data:</b> NWP Flow.ECMWF ERAInt Regional<br>
    <b>NAME Version:</b> NAME III (version 7.2)<br>
    <b>Release height:</b> 1651.000 to 6151.000m asl<br>
    <b>Release location:</b> 19.3600W   63.3700N<br>
    <b>Release rate:</b> 9.4444448E+07g/s<br>
    <b>Run time:</b> 0904UTC 20/07/2018<br>
    <b>Species:</b> VOLCANIC_ASH<br>
    <b>Species Category:</b> VOLCANIC<br>
    <b>Start of release:</b> 0000UTC 17/04/2010<br>
    <b>Title:</b> VA_Tutorial<br>
    <b>Conventions:</b> CF-1.5<br>
    <b>Quantity:</b> Air Concentration<br>
    <b>Time Av or Int:</b> 003 hr time averaged<br>
    </blockquote>

  <hr>
  <h4>Plots</h4>
    <h5>Altitude levels:</h5>
    <ul>
    <li><a href="#00500">00500</a></li>
    <li><a href="#01000">01000</a></li>

    </ul>
    <h5 id="00500">Altitude: 00500</h5>
      <table>
        <tr><td>
          <a href="00500/VA_Tutorial_Air_Concentration_00500_20100418030000.png">
            <img src="00500/VA_Tutorial_Air_Concentration_00500_20100418030000.png" width="640">
          </a>
        </td></tr>
        <tr><td>
          <a href="00500/VA_Tutorial_Air_Concentration_00500_20100418060000.png">
            <img src="00500/VA_Tutorial_Air_Concentration_00500_20100418060000.png" width="640">
          </a>
        </td></tr>
        </table>
      <hr>
    <h5 id="01000">Altitude: 01000</h5>
      <table>
        <tr><td>
          <a href="01000/VA_Tutorial_Air_Concentration_01000_20100418030000.png">
            <img src="01000/VA_Tutorial_Air_Concentration_01000_20100418030000.png" width="640">
          </a>
        </td></tr>
        <tr><td>
          <a href="01000/VA_Tutorial_Air_Concentration_01000_20100418060000.png">
            <img src="01000/VA_Tutorial_Air_Concentration_01000_20100418060000.png" width="640">
          </a>
        </td></tr>
        </table>
      <hr>

  </body>
</html>
""").strip()


def test_render_html_3d():
    # Arrange
    source = 'some source'
    metadata = {
        'created_by': 'plot_3d_cube',
        'attributes': {
            'End of release': '0800UTC 17/04/2010',
            'Forecast duration': '75 hours',
            'Met data': 'NWP Flow.ECMWF ERAInt Regional',
            'NAME Version': 'NAME III (version 7.2)',
            'Release height': '1651.000 to 6151.000m asl',
            'Release location': '19.3600W   63.3700N',
            'Release rate': '9.4444448E+07g/s',
            'Run time': '0904UTC 20/07/2018',
            'Species': 'VOLCANIC_ASH',
            'Species Category': 'VOLCANIC',
            'Start of release': '0000UTC 17/04/2010',
            'Title': 'VA_Tutorial',
            'Conventions': 'CF-1.5',
            'Quantity': 'Total deposition',
            'Time Av or Int': '078 hr time integrated'},
        'plots': {
            '20100418030000': 'VA_Tutorial_Total_deposition_20100418030000.png',
            '20100418060000': 'VA_Tutorial_Total_deposition_20100418060000.png'}
    }

    # Act
    html = render_html(source, metadata)

    # Assert
    assert _remove_whitespace(html) == _remove_whitespace(EXPECTED_3D)


def test_render_html_4d():
    # Arrange
    source = 'some source'
    metadata = {
        'created_by': 'plot_4d_cube',
        'attributes': {'End of release': '0800UTC 17/04/2010',
                       'Forecast duration': '75 hours',
                       'Met data': 'NWP Flow.ECMWF ERAInt Regional',
                       'NAME Version': 'NAME III (version 7.2)',
                       'Release height': '1651.000 to 6151.000m asl',
                       'Release location': '19.3600W   63.3700N',
                       'Release rate': '9.4444448E+07g/s',
                       'Run time': '0904UTC 20/07/2018',
                       'Species': 'VOLCANIC_ASH',
                       'Species Category': 'VOLCANIC',
                       'Start of release': '0000UTC 17/04/2010',
                       'Title': 'VA_Tutorial',
                       'Conventions': 'CF-1.5',
                       'Quantity': 'Air Concentration',
                       'Time Av or Int': '003 hr time averaged'},
        'plots': {
            '00500':
                {'20100418030000': 'VA_Tutorial_Air_Concentration_00500_20100418030000.png',
                 '20100418060000': 'VA_Tutorial_Air_Concentration_00500_20100418060000.png'},
            '01000':
                {'20100418030000': 'VA_Tutorial_Air_Concentration_01000_20100418030000.png',
                 '20100418060000': 'VA_Tutorial_Air_Concentration_01000_20100418060000.png'}
        }
    }

    # Act
    html = render_html(source, metadata)

    # Assert
    assert _remove_whitespace(html) == _remove_whitespace(EXPECTED_4D)


def _remove_whitespace(text):
    return " ".join(text.split())
