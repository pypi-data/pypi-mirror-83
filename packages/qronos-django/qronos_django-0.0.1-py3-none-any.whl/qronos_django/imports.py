from qronos_django.models import QRonosImportLog
from qronos_django.settings import QRONOS_LOGGING, QRONOS_ID_LOGGING, QRONOS_DATA_LOGGING
from qronos_django.tasks import process_import


def tracker_import(tracker_id, tracker_importer_id, unique_columns, data):
    import_type = QRonosImportLog.QRonosImportType.TRACKER
    if QRONOS_LOGGING:
        import_log = QRonosImportLog.objects.create(
            import_type=import_type,
            id_log=f"Tracker ID: {tracker_id}, Tracker Importer ID: {tracker_importer_id}" if QRONOS_ID_LOGGING else "LOGGING DISABLED",
            data_log=f"Unique Columns:\n{unique_columns}\n\nData:\n{data}" if QRONOS_DATA_LOGGING else "LOGGING DISABLED",
        )
        import_log_id = import_log.id
    else:
        import_log = None
        import_log_id = None
    process_import.delay(import_log_id, import_type, tracker_id, tracker_importer_id, unique_columns, data)
    return import_log


def stage_import(stage_id, stage_importer_id, data):
    import_type = QRonosImportLog.QRonosImportType.STAGE
    if QRONOS_LOGGING:
        import_log = QRonosImportLog.objects.create(
            import_type=import_type,
            id_log=f"Stage ID: {stage_id}, Stage Importer ID: {stage_importer_id}" if QRONOS_ID_LOGGING else "LOGGING DISABLED",
            data_log=f"Data:\n{data}" if QRONOS_DATA_LOGGING else "LOGGING DISABLED",
        )
        import_log_id = import_log.id
    else:
        import_log = None
        import_log_id = None
    process_import.delay(import_log_id, import_type, stage_id, stage_importer_id, data)
    return import_log
