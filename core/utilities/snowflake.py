import threading
import time
from dataclasses import dataclass, field

# Define constants.
EPOCH = 1727524500000  # Custom epoch (09-28-2024)
WORKER_ID_BITS = 5     # 5 bits for Worker ID
PROCESS_ID_BITS = 5    # 5 bits for Process ID
SEQUENCE_BITS = 12     # 12 bits for sequence within the same millisecond

# Bit masks and shifts.
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
MAX_PROCESS_ID = -1 ^ (-1 << PROCESS_ID_BITS)
MAX_SEQUENCE = -1 ^ (-1 << SEQUENCE_BITS)

WORKER_ID_SHIFT = SEQUENCE_BITS
PROCESS_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + PROCESS_ID_BITS


class SnowFlakeError(Exception):
    pass


@dataclass
class SnowflakeGenerator:
    """Snowflake ID generator for unique, ordered identifiers."""

    worker_id: int
    process_id: int
    sequence: int = field(default=0, init=False)
    last_timestamp: int = field(default=-1, init=False)
    lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def __post_init__(self):
        """
        Initialize Snowflake Generator with worker and process IDs.

        Args:
            worker_id (int): Identifier for the worker (0-31).
            process_id (int): Identifier for the process (0-31).
        """
        if not (0 <= self.worker_id <= MAX_WORKER_ID):
            raise ValueError(
                f'Worker ID must be between 0 and {MAX_WORKER_ID}'
            )
        if not (0 <= self.process_id <= MAX_PROCESS_ID):
            raise ValueError(
                f'Process ID must be between 0 and {MAX_PROCESS_ID}'
            )

    def _current_timestamp(self) -> int:
        """Return the current time in milliseconds."""
        return int(time.time() * 1000)

    def _wait_for_next_millis(self, last_timestamp: int) -> int:
        """Wait until the next millisecond."""
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def generate_id(self) -> int:
        """
        Generate a unique Snowflake ID.

        Returns:
            int: A unique 64-bit ID.

        Examples:
            >>> generator = SnowflakeGenerator(worker_id=1, process_id=1)
            >>> generator.generate_id()  # 12525664079873
        """
        with self.lock:
            timestamp = self._current_timestamp()

            if timestamp < self.last_timestamp:
                raise SnowFlakeError(
                    'Clock moved backwards. Refusing to generate ID.'
                )

            if self.last_timestamp == timestamp:
                # Same millisecond, increment the sequence.
                self.sequence = (self.sequence + 1) & MAX_SEQUENCE

                if self.sequence == 0:
                    # Sequence exhausted, wait for next millisecond.
                    timestamp = self._wait_for_next_millis(self.last_timestamp)
            else:
                # Reset sequence for a new millisecond.
                self.sequence = 0

            self.last_timestamp = timestamp

            # Construct the Snowflake ID.
            snowflake_id = (
                ((timestamp - EPOCH) << TIMESTAMP_SHIFT) |
                (self.process_id << PROCESS_ID_SHIFT) |
                (self.worker_id << WORKER_ID_SHIFT) |
                self.sequence
            )
            return snowflake_id
