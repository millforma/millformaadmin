from django.db import models

from main.models.base import BaseModel


class DocumentType(BaseModel):
    EMARGEMENT = 1
    CONTRAT_FORMATEUR = 2
    CONVOCATION = 3
    QCM = 4
    REGLEMENT = 5
    COMPTE_RENDU = 6
    ORDRE_MISSION = 7
    ATTESTATION_FIN_STAGE = 8
    CONVENTION = 9
    BON_COMMANDE = 10
    KBIS = 11
    RIB = 12
    INSEE = 13

    DOCUMENT_TYPE_CHOICES = [
        (EMARGEMENT, "Emargement"),
        (CONTRAT_FORMATEUR, "Contrat de partenariat formateur"),
        (CONVOCATION, "Convocation"),
        (QCM, "Qcm"),
        (REGLEMENT, "Reglement interieur"),
        (COMPTE_RENDU, "Compte Rendu de formation"),
        (ORDRE_MISSION, "Ordre de mission"),
        (ATTESTATION_FIN_STAGE, "Attestation de fin de stage"),
        (BON_COMMANDE, "Bon de commande"),
        (KBIS, "Kbis"),
        (RIB, "Rib"),
        (INSEE, "Declaration Insee"),
    ]

    name = models.IntegerField(
        choices=DOCUMENT_TYPE_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"{self.str_clean(self.name)}"
