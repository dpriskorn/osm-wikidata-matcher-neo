import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export interface ObjectTypeInfo {
  object_type: string
  label: string
}

export interface CandidateInfo {
  qid: string
  label: string
  country_label: string | null
}

export interface MatchInfo {
  osm_id: string
  osm_type: string
  osm_name: string
  similarity: number
  osm_url: string
}

export interface MatchResponse {
  qid: string
  label: string
  matches: MatchInfo[]
}

export async function getObjectTypes(): Promise<ObjectTypeInfo[]> {
  const { data } = await api.get('/types')
  return data
}

export async function getCandidates(type: string): Promise<CandidateInfo[]> {
  const { data } = await api.get(`/types/${type}/candidates`)
  return data
}

export async function getMatches(type: string, qid: string): Promise<MatchResponse> {
  const { data } = await api.get(`/types/${type}/candidates/${qid}/matches`)
  return data
}

export async function confirmMatch(
  type: string,
  qid: string,
  osmId: string,
  osmType: string,
  osmName: string
): Promise<void> {
  await api.post(`/types/${type}/candidates/${qid}/confirm`, {
    osm_id: osmId,
    osm_type: osmType,
    osm_name: osmName,
  })
}

export async function rejectMatch(
  type: string,
  qid: string,
  reason?: string
): Promise<void> {
  await api.post(`/types/${type}/candidates/${qid}/reject`, {
    reason,
  })
}
