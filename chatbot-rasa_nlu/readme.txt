python3.11 -m venv env
source ./env/bin/activate
pip install rasa-pro
export RASA_PRO_LICENSE="your-rasa-pro-license-key"
rasa init
rasa run actions
rasa train
rasa inspect/shell
