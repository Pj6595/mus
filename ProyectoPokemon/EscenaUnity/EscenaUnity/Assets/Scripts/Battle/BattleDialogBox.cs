/* 
 * Este script se encarga de la implementaci�n de la clase BattleDialogBox, que controla la caja de  texto que
 * funciona como interfaz del juego. Activa/desactiva los men�s y di�logos, resalta las opciones que est� seleccionando
 * el jugador, etc.
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BattleDialogBox : MonoBehaviour
{
	[SerializeField] Text dialogText;
	[SerializeField] int lettersPerSecond;

	[SerializeField] GameObject actionSelector;
	[SerializeField] GameObject moveSelector;
	[SerializeField] GameObject moveDetails;
	[SerializeField] GameObject choiceBox;

	[SerializeField] List<Text> actionTexts;
	[SerializeField] List<Text> moveTexts;

	[SerializeField] Text ppText;
	[SerializeField] Text typeText;

	[SerializeField] Text yesText;
	[SerializeField] Text noText;

	[SerializeField] Color highlightedColor;

	public void SetDialog(string dialog)
	{
		dialogText.text = dialog;
	}

	public IEnumerator TypeDialog(string dialog)
	{
		dialogText.text = "";
		foreach(var letter in dialog.ToCharArray())
		{
			dialogText.text += letter;
			yield return new WaitForSeconds(1f / lettersPerSecond);
		}

		yield return new WaitForSeconds(1f);
	}

	public void EnableDialogText(bool enabled)
	{
		dialogText.enabled = enabled;
	}

	public void EnableActionSelector(bool enabled)
	{
		actionSelector.SetActive(enabled);
	}

	public void EnableMoveSelector(bool enabled)
	{
		moveSelector.SetActive(enabled);
		moveDetails.SetActive(enabled);
	}

	public void EnableChoiceBox(bool enabled)
	{
		choiceBox.SetActive(enabled);
	}

	public void UpdateActionSelection(int selectedAction)
	{
		for (int i = 0; i < actionTexts.Count; i++)
		{
			if (i == selectedAction)
			{
				actionTexts[i].color = highlightedColor;
			}
			else actionTexts[i].color = Color.black;
		}
	}

	public void UpdateMoveSelection(int selectedMove, Move move)
	{
		for (int i = 0; i < moveTexts.Count; i++)
		{
			if (i == selectedMove)
			{
				moveTexts[i].color = highlightedColor;
			}
			else
			{
				moveTexts[i].color = Color.black;
			}
		}

		ppText.text = $"PP {move.PP}/{move.Base.PP}";
		typeText.text = move.Base.Type.ToString();

		if (move.PP == 0)
			ppText.color = Color.red;
		else ppText.color = Color.black;
	}

	public void SetMoveNames(List<Move> moves)
	{
		for(int i = 0; i < moveTexts.Count; i++)
		{
			if (i < moves.Count) moveTexts[i].text = moves[i].Base.Name;
			else moveTexts[i].text = "-";
		}
	}

	public void UpdateChoiceBox(bool yesSelected)
	{
        if (yesSelected)
        {
			yesText.color = highlightedColor;
			noText.color = Color.black;
        }
        else
        {
			yesText.color = Color.black;
			noText.color = highlightedColor;
		}
	}
}