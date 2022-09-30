
ASPECT=${1:-"overall"}
OUTPUT_FILE=${2:-"overall.words"}

cat output.json | jq -r --arg ASPECT $ASPECT "to_entries | sort_by(.value.$ASPECT) | reverse | .[].key" > $OUTPUT_FILE
