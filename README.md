# kalliope-trigger-openww
<p>Openwakeword Trigger for Kalliope, see details at https://github.com/dscripka/openWakeWord</p>

<b>Installaion:</b>
<p>
pip install openwakeword<br/>
Create a directory openww in kalliope_base/triggers<br/>
Copy all the .py files into kalliope_base/triggers/openww<br/>
Create a directory oww_models in kalliope_home/resources/triggers<br/>
Change into the above directory then,<br/>
In python:
</p>
<pre>
import openwakeword
from openwakeword.model import Model
openwakeword.utils.download_models()
</pre>
<p>
Copy all the .py files into kalliope_base/trigger/openww<br/>
</p>
<p>In settings.yml add the following to the triggers section</p>
<pre>
default_trigger: "openww"
triggers:
- openww:
      model_file: "trigger/oww_models/alexa_v0.1.onnx"
      engine: "onnx"
</pre>


