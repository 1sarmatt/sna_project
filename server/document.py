# document.py (updated)
import time
import uuid
from typing import List, Dict, Any
from db import documents_collection

class TextOperation:
    def __init__(self, type: str, position: int, text: str = '', length: int = 0,
                 deleted_text: str = '', username: str = '', timestamp=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.type = type
        self.position = position
        self.text = text
        self.length = length
        self.deleted_text = deleted_text
        self.timestamp = timestamp or time.time() * 1000
        self.username = username

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return TextOperation(**data)

class Document:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.text = ''
        self.revision = 0
        self.clients = {}
        self.history: List[TextOperation] = []
        self.load_from_db()

    def load_from_db(self):
        doc = documents_collection.find_one({'session_id': self.session_id})
        if doc:
            self.text = doc.get('text', '')
            self.revision = doc.get('revision', 0)
            self.history = [TextOperation.from_dict(op) for op in doc.get('history', [])]

    def save_to_db(self):
        documents_collection.update_one(
            {'session_id': self.session_id},
            {
                '$set': {
                    'text': self.text,
                    'revision': self.revision,
                    'history': [op.to_dict() for op in self.history]
                }
            },
            upsert=True
        )

    def undo_last_operation(self):
        if not self.history:
            return None

        last_op = self.history.pop()
        inverse_ops = []

        if last_op.type == 'insert':
            inverse_ops.append(TextOperation(
                type='delete',
                position=last_op.position,
                length=len(last_op.text),
                deleted_text=last_op.text
            ))
        elif last_op.type == 'delete':
            inverse_ops.append(TextOperation(
                type='insert',
                position=last_op.position,
                text=last_op.deleted_text
            ))

        for op in inverse_ops:
            if op.type == 'insert':
                self.text = self.text[:op.position] + op.text + self.text[op.position:]
            elif op.type == 'delete':
                self.text = self.text[:op.position] + self.text[op.position + op.length:]

        self.revision -= 1
        self.save_to_db()
        return [op.to_dict() for op in inverse_ops]

    def apply_operations(self, client_id: str, client_revision: int, operations: List[Dict]) -> List[Dict]:
        incoming_ops = [TextOperation(**op) for op in operations]
        if client_revision < self.revision:
            missed_ops = self.history[client_revision:]
            transformed_ops = self._transform_operations(incoming_ops, missed_ops)
        else:
            transformed_ops = incoming_ops
        result_ops = []

        for op in transformed_ops:
            if op.type == 'insert':
                self.text = self.text[:op.position] + op.text + self.text[op.position:]
            elif op.type == 'delete':
                op.deleted_text = self.text[op.position:op.position + op.length]
                self.text = self.text[:op.position] + self.text[op.position + op.length:]
            self.history.append(op)
            result_ops.append(op.to_dict())

        self.revision += len(result_ops)
        self.clients[client_id] = self.revision
        self.save_to_db()
        return result_ops

    def _transform_operations(self, incoming_ops: List[TextOperation], missed_ops: List[TextOperation]) -> List[TextOperation]:
        transformed_ops = incoming_ops.copy()

        for missed_op in missed_ops:
            for i, op in enumerate(transformed_ops):
                if op.position < missed_op.position:
                    continue
                elif op.position > missed_op.position:
                    if missed_op.type == 'insert':
                        op.position += len(missed_op.text)
                    elif missed_op.type == 'delete':
                        op.position = max(missed_op.position, op.position - missed_op.length)
                else:
                    if op.type == 'insert' and missed_op.type == 'insert':
                        if op.id > missed_op.id:
                            op.position += len(missed_op.text)
                    elif op.type == 'delete' and missed_op.type == 'insert':
                        op.position += len(missed_op.text)
                    elif op.type == 'insert' and missed_op.type == 'delete':
                        op.position = max(missed_op.position, op.position)

        return transformed_ops

    def get_edit_history(self) -> List[Dict]:
        return [op.to_dict() for op in self.history]
