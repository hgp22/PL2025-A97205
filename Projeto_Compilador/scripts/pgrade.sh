#!/bin/bash

TEST_DIR="test"
SCRIPT_DIR="src"
TEST_FILES=("$TEST_DIR/ex{1..7}.pp")
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
OUTPUT_FILE="out/test_report_$TIMESTAMP.txt"

TEST_TYPES=("lexical:$SCRIPT_DIR/analex.py:>>:Validação do Analisador Léxico")

total_errors_lexical=0
total_lines_lexical=0

run_test() {
    local test_name="$1"
    local script="$2"
    local error_pattern="$3"
    local file="$4"

    if [[ ! -f "$script" ]]; then
        echo "Script $script not found, skipping $test_name test for $file..." >&2
        return 1
    fi
    if [[ ! -f "$file" ]]; then
        echo "File $file not found, skipping $test_name test..." >&2
        return 1
    fi

    local errors=$(python3 "$script" < "$file" | grep "$error_pattern" | wc -l)
    local lines=$(wc -l < "$file")

    local percentage=0
    local correctness=100
    if [[ $lines -gt 0 ]]; then
        percentage=$(echo "scale=2; ($errors / $lines) * 100" | bc)
        correctness=$(echo "scale=2; 100 - $percentage" | bc)
    fi

    echo "$errors:$lines:$percentage:$correctness"
}

print_report() {
    local output=""
    output+="Analysis Report\n"
    output+="================\n\n"

    for test_config in "${TEST_TYPES[@]}"; do
        IFS=':' read -r test_name script error_pattern description <<< "$test_config"
        output+="$description\n"
        output+="----------------------------------------\n"

        total_errors_lexical=0
        total_lines_lexical=0

        local file_count=0
        for file in "${TEST_FILES[@]}"; do
            for expanded_file in $(eval echo "$file"); do
                if [[ -f "$expanded_file" ]]; then
                    ((file_count++))
                    result=$(run_test "$test_name" "$script" "$error_pattern" "$expanded_file")
                    if [[ $? -eq 0 ]]; then
                        IFS=':' read -r errors lines percentage correctness <<< "$result"
                        output+="File: $expanded_file\n"
                        output+="Errors: $errors\n"
                        output+="Total Lines: $lines\n"
                        output+="Error Percentage: $percentage%\n"
                        output+="Correctness Grade: $correctness%\n\n"

                        total_errors_lexical=$((total_errors_lexical + errors))
                        total_lines_lexical=$((total_lines_lexical + lines))
                    else
                        output+="Failed to process $expanded_file\n\n"
                    fi
                else
                    output+="File $expanded_file not found, skipping...\n\n"
                fi
            done
        done

        if [[ $file_count -eq 0 ]]; then
            output+="No test files found in $TEST_DIR. Please ensure files exist.\n\n"
        fi

        local overall_percentage=0
        local overall_correctness=100
        if [[ $total_lines_lexical -gt 0 ]]; then
            overall_percentage=$(echo "scale=2; ($total_errors_lexical / $total_lines_lexical) * 100" | bc)
            overall_correctness=$(echo "scale=2; 100 - $overall_percentage" | bc)
        fi

        output+="Summary for $description\n"
        output+="Total Errors: $total_errors_lexical\n"
        output+="Total Lines: $total_lines_lexical\n"
        output+="Overall Error Percentage: $overall_percentage%\n"
        output+="Overall Correctness Grade: $overall_correctness%\n\n"
    done

    mkdir -p "$(dirname "$OUTPUT_FILE")"

    echo -e "$output"
    echo -e "$output" > "$OUTPUT_FILE"
    if [[ $? -eq 0 ]]; then
        echo "Report saved to $OUTPUT_FILE"
    else
        echo "Failed to save report to $OUTPUT_FILE" >&2
        exit 1
    fi
}

main() {
    if [[ ${#TEST_TYPES[@]} -eq 0 ]]; then
        echo "No test types defined. Please configure TEST_TYPES in the script." >&2
        exit 1
    fi

    print_report
}

main
