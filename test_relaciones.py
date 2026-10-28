import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from modelos import Base, CategoriaModel, EtiquetaModel, ProductoModel


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    with Session() as session:
        yield session

    engine.dispose()


def test_producto_puede_tener_varias_etiquetas(db_session):
    categoria = CategoriaModel(nombre="Electrodomésticos")

    producto = ProductoModel(
        nombre="Cafetera",
        precio=120.0,
        categoria=categoria,
    )

    etiqueta_oferta = EtiquetaModel(nombre="Oferta")
    etiqueta_nuevo = EtiquetaModel(nombre="Nuevo")

    producto.etiquetas.extend([etiqueta_oferta, etiqueta_nuevo])

    db_session.add(producto)
    db_session.commit()

    prod_db = db_session.scalars(
        select(ProductoModel).filter_by(nombre="Cafetera")
    ).first()

    assert prod_db is not None
    assert len(prod_db.etiquetas) == 2
    assert {etiqueta.nombre for etiqueta in prod_db.etiquetas} == {
        "Oferta",
        "Nuevo",
    }


def test_etiqueta_puede_tener_varios_productos(db_session):
    categoria = CategoriaModel(nombre="Electrodomésticos")

    producto = ProductoModel(
        nombre="Cafetera",
        precio=120.0,
        categoria=categoria,
    )

    etiqueta = EtiquetaModel(nombre="Oferta")
    producto.etiquetas.append(etiqueta)

    db_session.add(producto)
    db_session.commit()

    tag_db = db_session.scalars(
        select(EtiquetaModel).filter_by(nombre="Oferta")
    ).first()

    assert tag_db is not None
    assert tag_db.productos[0].nombre == "Cafetera"
