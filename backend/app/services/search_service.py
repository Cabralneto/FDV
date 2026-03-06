from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.entities import CronogramaAtividade, DocumentoLD, Fornecedor, Pendencia, RequisicaoMaterial


def global_search(db: Session, query: str):
    term = f"%{query}%"
    return {
        "documentos": db.query(DocumentoLD).filter(or_(DocumentoLD.numero.ilike(term), DocumentoLD.status.ilike(term))).limit(10).all(),
        "cronograma": db.query(CronogramaAtividade).filter(or_(CronogramaAtividade.atividade_codigo.ilike(term), CronogramaAtividade.descricao.ilike(term))).limit(10).all(),
        "fornecedores": db.query(Fornecedor).filter(Fornecedor.nome.ilike(term)).limit(10).all(),
        "pendencias": db.query(Pendencia).filter(Pendencia.titulo.ilike(term)).limit(10).all(),
        "requisicoes": db.query(RequisicaoMaterial).filter(RequisicaoMaterial.codigo.ilike(term)).limit(10).all(),
    }
