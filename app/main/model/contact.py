import datetime
import uuid
from pyphonetics import Soundex

from app.main.services import db, flask_bcrypt
from app.main.util.hashutils import HashUtils


class Contact(db.Model):
    """ Contact Model for storing anagraphic details """
    __tablename__ = "contact"

    id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True) #as str to make it compatible with more dbs, if only postgres is used, then UUID is fine
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    mother_first_name = db.Column(db.String(255), unique=False, nullable=True)
    father_first_name = db.Column(db.String(255), unique=False, nullable=True)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    secret = db.Column(db.LargeBinary(), unique=False, nullable=False) #256-bit noise in 32 8-bit words
    phonetic_id = db.Column(db.String(28), unique=True, nullable=False) #concat of phonetic names and YYYYMMDD date of birth, separator: "-"
    uscadi = db.Column(db.String(64), unique=True, nullable=False) #hex digest of 256 bits
    created_on = db.Column(db.DateTime, nullable=False)

    @property
    def fresh_phonetic_id(self):
        """
        Use the phonetics library to build the phonetic parts, the concat with the YYYYMMDD date of birth

        Must be copied into phoenetic_id to allow for querying and checking uniqueness
        """
        try:
            soundex_first_name = Soundex().phonetics(self.first_name)
            soundex_last_name = Soundex().phonetics(self.last_name)
            soundex_mother_fisrt_name = Soundex().phonetics(self.mother_first_name)
            soundex_father_fisrt_name = Soundex().phonetics(self.father_first_name)
            formatted_dob = self.date_of_birth.strftime("%Y%m%d")
            return (soundex_first_name+"-"+soundex_last_name+"-"+soundex_mother_fisrt_name+"-"+soundex_father_fisrt_name+"-"+formatted_dob)
        except Exception as general_exception:
            print("An Exception occured: " + str(general_exception))
            #TODO: should never happen, but probably better to raise anyway
            return general_exception

    @property
    def fresh_uscadi(self):
        """
        hash the phonetic_id concatenated with the secret (utf-8 formatted) to create the uscadi id
        """
        try:
            p_id = self.fresh_phonetic_id
            b = bytearray(p_id.encode()) #defaults to utf-8 encoding
            b+=(bytearray(self.secret))
            message = bytes(b)
            hu = HashUtils()
            hex_uscadi = hu.digest(message).hex()
            return hex_uscadi
        except Exception as general_exception:
            print("An Exception occured: " + str(general_exception))
            #TODO: should never happen, but probably better to raise anyway
            return general_exception
    


    def __repr__(self):
        return "<Contact ID '{}', name: '{}{}'>".format(self.phonetic_id, self.first_name, self.last_name)

    