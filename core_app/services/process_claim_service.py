import csv
import codecs
from fastapi import HTTPException, status
from core_app.serializer import ClaimFileModel
from core_app.models import Claim


class ProcessClaiFile:
    def execute(self, file,db):
        csv_reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
        valid_records = []
        errors = []
        for row in csv_reader:
            try:
                validated_data = ClaimFileModel(**row)
                # here i think we should have validation that allowed fees should not greater than all other fields
                # net fee” = “provider fees” + “member coinsurance” + “member copay” - “Allowed fees”*
                net_fees  = (validated_data.provider_fees +
                            validated_data.member_coinsurance +
                            validated_data.member_copay - validated_data.allowed_fees)
                claim_obj = Claim(
                    submitted_procedure=validated_data.submitted_procedure,
                    quadrant=validated_data.quadrant,
                    plan_group=validated_data.plan_group,
                    subscriber=validated_data.subscriber,
                    provider_npi=validated_data.provider_npi,
                    provider_fees=validated_data.provider_fees,
                    allowed_fees=validated_data.allowed_fees,
                    member_coinsurance=validated_data.member_coinsurance,
                    member_copay=validated_data.member_copay,
                    service_date=validated_data.service_date,
                    net_fee=net_fees)

                valid_records.append(claim_obj)

            except Exception as e:
                errors.append({"row": csv_reader.line_num, "error":  ",".join([i['msg'] for i in e.errors()])})

        file.file.close()
        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"message": "fields validation failed ", "errors": errors}
            )
        db.add_all(valid_records)
        db.commit()
        return {"saved_records": len(valid_records), "errors": errors}