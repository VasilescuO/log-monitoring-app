from log_parser import parser, app_logger


if __name__ == "__main__":
    app_logger.get_logger().info("Starting log parser...")
    # Define the path to the log file
    log_file_path = 'logs/logs.log'  # Update with your actual log file path

    app_logger.get_logger().info("Parsing log file: %s", log_file_path)
    # Parse the log file
    log_lines = parser.parse_log_file(log_file_path)

    app_logger.get_logger().info("Calculating task durations...")
    # Evaluate durations
    durations, unfinished_lines = parser.evaluate_durations(log_lines)

    app_logger.get_logger().info("Writing output file...")
    # Print the results
    print("\nFinished tasks:")
    for duration in durations:
        print(duration)

    print("\nUnfinished tasks:")
    for line in unfinished_lines:
        print(line)