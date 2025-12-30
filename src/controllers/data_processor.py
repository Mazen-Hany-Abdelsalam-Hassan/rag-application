from .data_processing_controllers import SimpleProcessing

class DataProcessor:
    PROCESSING = {
        "SimpleProcessing": SimpleProcessing
    }

    @classmethod
    def load_processor(
        cls,
        processing_method: str
    ):
        processor = cls.PROCESSING.get(processing_method)
        if not processor:
            return False

        return processor
