
from operator import or_

from flask import render_template, session

from app import db
from app.models import FuncionarioProjeto, LancamentoHoras, Funcionario, User, Ponto
from . import relatorio


@relatorio.route('/minhasHoras')
def minhashoras():
    user = User.query.filter_by(email=session["session_name"]).first_or_404()
    funcionario = Funcionario.query.filter(Funcionario.matricula == user.id).first()

    minhasHoras= Ponto.query.filter(Ponto.funcionario_id == funcionario.id).order_by(Ponto.data_lancamento)

    #totalHoras = Ponto.query.Select([Ponto.hora_fim_1 - Ponto.hora_inicio_1]).filter(Ponto.funcionario_id == funcionario.id and Ponto.data_lancamento.strftime("%m")).order_by(Ponto.data_lancamento)

    return render_template('relatorio/relatorioMinhasHoras.html', minhasHoras=minhasHoras)

@relatorio.route('/meusProjetos')
def meusprojetos():
    user = User.query.filter_by(email=session["session_name"]).first_or_404()
    funcionario = Funcionario.query.filter(Funcionario.matricula == user.id).first()

    sqlCordenador = db.session.query(FuncionarioProjeto.id).filter(FuncionarioProjeto.funcionario_id == funcionario.id,
                                                    FuncionarioProjeto.cordenador == 1).subquery()


    minhasHoras = LancamentoHoras.query.join(LancamentoHoras.projetos).join(LancamentoHoras.atividades).join(LancamentoHoras.funcionarios).\
        filter(or_(LancamentoHoras.id.in_((sqlCordenador)), LancamentoHoras.funcionario_id == funcionario.id))


    meusProjetos = LancamentoHoras.query.join(LancamentoHoras.projetos)

    return render_template('relatorio/relatorioMeusProjetos.html', meusProjetos=minhasHoras)