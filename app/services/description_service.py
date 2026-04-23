import json
import re
from app.extensions import SessionLocal
from app.models.product_request import ProductRequest
from app.models.description import Description
from app.services.llm_service import generate_from_llm


def _parse_description_response(result):
    content = result.get("response") if isinstance(result, dict) else result
    if not isinstance(content, str):
        raise Exception("Invalid JSON from LLM: response must be a string")

    content = re.sub(r"```(?:json)?\s*|\s*```", "", content).strip()
    parsed = json.loads(content)

    description = parsed.get("description")
    if not isinstance(description, str) or not description.strip():
        raise Exception("Invalid JSON from LLM: 'description' is missing")

    return description.strip()


def _serialize_row(desc, req):
    return {
        "id": desc.id,
        "content": desc.content,
        "created_at": desc.created_at.isoformat(),
        "request": {
            "id": req.id,
            "product_name": req.product_name,
            "features": [item.strip() for item in req.features.split(",") if item.strip()],
            "platform": req.platform,
            "tone": req.tone,
            "created_at": req.created_at.isoformat(),
        },
    }


def create_description(product_name: str, features: list[str], platform: str, tone: str):
    session = SessionLocal()
    try:
        features_text = ", ".join(features)
        prompt = f"""
        Kamu adalah product description writer profesional.
        Buat 1 deskripsi produk e-commerce dalam format JSON valid HANYA.
        Data produk:
        - Nama produk: {product_name}
        - Fitur utama: {features_text}
        - Platform target: {platform}
        - Gaya bahasa: {tone}

        Aturan:
        - Tulis deskripsi siap pakai untuk marketplace.
        - Panjang sekitar 80-140 kata.
        - Fokus pada manfaat produk dan ajakan membeli yang natural.
        - Output HANYA JSON, TANPA TEKS LAIN.
        - Jangan tambahkan markdown code fence.
        - Response harus valid JSON yang bisa diparsing langsung.

        Format output WAJIB:
        {{
            "description": "..."
        }}
        """

        result = generate_from_llm(prompt)
        description_text = _parse_description_response(result)

        request_row = ProductRequest(
            product_name=product_name,
            features=features_text,
            platform=platform,
            tone=tone,
        )
        session.add(request_row)
        session.commit()

        description_row = Description(content=description_text, request_id=request_row.id)
        session.add(description_row)
        session.commit()

        return _serialize_row(description_row, request_row)

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_all_descriptions():
    session = SessionLocal()
    try:
        rows = (
            session.query(Description, ProductRequest)
            .join(ProductRequest, ProductRequest.id == Description.request_id)
            .order_by(Description.id.desc())
            .all()
        )

        data = [_serialize_row(desc, req) for desc, req in rows]
        return {"total": len(data), "data": data}
    finally:
        session.close()


def delete_description_by_id(description_id: int):
    session = SessionLocal()
    try:
        row = session.query(Description).filter(Description.id == description_id).first()
        if row is None:
            return False

        request_id = row.request_id
        session.delete(row)
        session.flush()

        remaining = session.query(Description).filter(Description.request_id == request_id).count()
        if remaining == 0:
            req = session.query(ProductRequest).filter(ProductRequest.id == request_id).first()
            if req is not None:
                session.delete(req)

        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
